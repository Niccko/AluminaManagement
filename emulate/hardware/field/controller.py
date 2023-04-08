from .sensor import Sensor
from threading import Thread
import json

class PLC:
    def __init__(self):
        self.tick = 0
        self.inputs = {}
        self.outputs = {}
        self.init_prg = None
        self.tick_prg = None
        self.data_send_prg = None

    def add_sensor(self, port, sensor):
        self.inputs[port] = sensor

    def add_executor(self, port, executor):
        self.outputs[port] = executor

    def send_sensor_value(self, port):
        sensor = self.get_sensor_info(port)
        return {
            "input_source_id": sensor.id,
            "value": self.get(port)
        }

    def send_sensors_values(self):
        for port in self.inputs:
            if isinstance(self.inputs[port], Sensor):
                yield self.send_sensor_value(port)

    def get_sensor_info(self, port) -> Sensor:
        if not self.inputs.get(port):
            raise Exception(f'[CONTROLLER ERROR] Port {port} is not assigned.')
        return self.inputs[port]

    def get(self, port):
        if not self.inputs.get(port):
            raise Exception(f'[CONTROLLER ERROR] Port {port} is not assigned.')
        return self.inputs[port].evaluate(self.tick)

    def write_to_analog(self, port, value):
        if not self.outputs.get(port):
            raise Exception(f'[CONTROLLER ERROR] Port {port} is not assigned.')
        return self.outputs[port].work(value)

    def set_init_func(self, func):
        self.init_prg = func

    def set_tick_func(self, func):
        self.tick_prg = func

    def start(self):
        if self.init_prg:
            self.init_prg(self)
        if not self.tick_prg:
            raise Exception('[CONTROLLER ERROR] Update function is not set.')

        def loop():
            while True:
                self.tick_prg(self)
                self.tick += 1

        Thread(target=loop).start()
