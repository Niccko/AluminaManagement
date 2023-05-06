import socket
from utils.events.event_bus import EventBus
import json
from threading import Thread
from modules.logger import *
import global_vars


def handle(data):
    str_data = data.strip().decode("utf-8")
    for chunk in str_data.split("#"):
        if not chunk:
            continue
        data = json.loads(chunk)
        event_type = data["event_type"]
        del data["event_type"]
        if event_type == "input":
            print(data)
        EventBus.invoke(event_type, **data)


def listener(client, address):
    global hardware_connection
    info(f"Accepted connection from: {address}")
    global_vars.hardware_connected = True
    EventBus.invoke("bunkers_updated")
    hardware_connection = client
    try:
        while True:
            try:
                data = client.recv(32768)
                if not data:
                    continue
            except Exception as e:
                global_vars.hardware_connected = False
                EventBus.invoke("bunkers_updated")
                error(f"Связь с оборудованием потеряна: {e}")
                break
            handle(data)


    finally:
        global_vars.hardware_connected = False
        client.close()


def get_hardware_client():
    return hardware_connection


def serve(done):
    EventBus.add_event("load")
    EventBus.add_event("feed")
    EventBus.add_event("input")
    EventBus.add_event("process_start")
    EventBus.add_event("init_topology")
    while not done.is_set():
        info("Server is listening for connections...")
        client, address = s.accept()
        Thread(target=listener, args=(client, address)).start()
    s.close()


host = socket.gethostname()
port = 9999

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", port))
s.listen(1)
hardware_connection = None
