from enum import Enum


class SensorType(Enum):
    NONE = 0
    TEMPERATURE = 1
    LEVEL = 2
    ROTATION_SPEED = 3
    HUMIDITY = 4
    OIL_LEVEL = 5
    ALUMINA_LEVEL = 6


class Sensor():
    def __init__(self, sensor_type, name, con_type, output_func,  id = 0):
        self.name = name
        self.id = id
        self.type: SensorType = sensor_type
        self.connection_type = con_type
        self.evaluate = output_func
