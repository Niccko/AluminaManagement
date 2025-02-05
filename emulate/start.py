from traceback import print_tb
from hardware.field import *
from hardware.field.nodes import *
import time
import tcp
from threading import Thread
import os, json
from pprint import pprint
from utils.events.event_bus import EventBus
from datetime import datetime

plc = PLC()

bunkers = []
aas = []
level_sensors = []


def init_topology(a, b):
    global bunkers, aas, level_sensors
    for i in range(a):
        bunkers.append(MainBunker(i + 1, 20000))
        level_sensors.append(
            Sensor(SensorType.ALUMINA_LEVEL, f"Сенсор {i}", "ANALOG", lambda t, b=bunkers[i]: b.level, id=i + 1))
        plc.add_sensor(f"A{i}", level_sensors[i])

    for i in range(a, a + b):
        aas.append(AASBunker(i + 1, 600, bunkers[(i - a) % a]))
        level_sensors.append(
            Sensor(SensorType.ALUMINA_LEVEL, f"Сенсор {i}", "ANALOG", lambda t, b=aas[i - a]: b.level, id=i + 1))
        plc.add_sensor(f"A{i}", level_sensors[i])


def form_topology_description():
    global bunkers, aas, level_sensors
    data = {"sensors": [
        {
            "input_source_id": sensor.id,
            "data_type": "DOUBLE",
            "input_name": sensor.name
        }
        for sensor in level_sensors
    ], "bunkers": [
        {
            "bunker_id": a.id,
            "is_aas": True,
            "capacity": a.capacity,
            "input_source_id": a.id,
        }
        for a in aas
    ]}

    data["bunkers"].extend([
        {
            "bunker_id": b.id,
            "is_aas": False,
            "capacity": b.capacity,
            "input_source_id": b.id,
        }
        for b in bunkers
    ])
    return data


def data_send(self):
    def feed(bunker_id, quantity):
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        tcp.write(self.client,
                  json.dumps({"feed_dt": dt, "event_type": "feed", "bunker_id": bunker_id, "quantity": quantity}))

    def load(bunker_id, quantity, type, source_bunker_id):
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        tcp.write(self.client, json.dumps(
            {"load_dt": dt, "event_type": "load", "bunker_id": bunker_id, "quantity": quantity, "type": type,
             "source_bunker_id": source_bunker_id}))

    EventBus.subscribe("alumina_feed", feed)
    EventBus.subscribe("alumina_load", load)

    while True:
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        sensor_data = [x for x in self.send_sensors_values()]
        tcp.write(self.client, json.dumps({"event_type": "input", "measure_dt": dt, "data": sensor_data}))
        time.sleep(1)


def message_handler(self):
    while True:

        msg = self.client.recv(1024).decode('utf-8')
        if not msg:
            continue
        for chunk in msg.split("#"):
            print(chunk)
            if not chunk:
                continue
            data = json.loads(chunk)
            if data.get("event_type") == "aas_load":
                data = data.get("data")
                a = aas[data.get("bunker_id") - len(bunkers) - 1]
                print(f"=== LOADING TO AAS {data.get('bunker_id')} ===")
                if not data.get("source_silage_id"):
                    continue
                source = bunkers[data.get("source_silage_id") - 1]
                source.give(a)
                print(f"=== DONE LOADING TO AAS {data.get('bunker_id')} ===")


def init(self):
    global bunkers
    EventBus.add_event("alumina_load")
    EventBus.add_event("alumina_feed")
    self.client, recv_thread = tcp.start_client(message_handler, args=(self,))
    recv_thread.start()
    init_topology(4, 60)
    tcp.write(self.client, json.dumps({"event_type": "process_start"}))
    time.sleep(0.1)
    tcp.write(self.client, json.dumps({"event_type": "init_topology", "data": form_topology_description()}))
    time.sleep(0.1)
    Thread(target=data_send, args=(self,)).start()
    for i in bunkers:
        i.restore()
    time.sleep(1)
    for i in aas:
        i.active = True
    # pprint(form_topology_description())
    pass


def tick(self):
    for bunker in aas:
        bunker.tick()
    time.sleep(1)


plc.set_init_func(init)
plc.set_tick_func(tick)
plc.start()
