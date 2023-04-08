from random import randint
from utils.events.event_bus import EventBus
from time import time
EventBus.add_event("alumina_load")
EventBus.add_event("alumina_feed")

class AASBunker:
    def __init__(self, id, capacity, source):
        self.id = id
        self.capacity = capacity
        self.level = 0
        self.time = 0
        self.source = source
        self.active = False

    def tick(self):
        if not self.active:
            return
        self.time += 1
        if self.level < 50:
            self.source.give(self)
        if self.time % randint(1,5) == 0 and self.level>=25:
            EventBus.invoke("alumina_feed", bunker_id = self.id, quantity = 25)
            self.level -= 25
            self.level = max(0, self.level)
        

class MainBunker():
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.level = 0
        self.time = 0

    def give(self, aas):
        if self.level >= 500:
            aas.level += 500
            aas.level = min(aas.level, aas.capacity)
            self.level -= 500
            self.level = max(0, self.level)
            EventBus.invoke("alumina_load", bunker_id = aas.id, quantity = 500, source_bunker_id=self.id, type = 1)
            EventBus.invoke("alumina_feed", bunker_id = self.id, quantity = 500)
    
    def restore(self):
        self.level = self.capacity
        EventBus.invoke("alumina_load", bunker_id = self.id, quantity = self.capacity, source_bunker_id=None, type = 1)


class Centriguge():
    def __init__(self):
        self.rotation_speed = 0
        self.temperature = 0
        self.enabled = False

    def apply_rotation_power(self, power):
        self.rotation_speed += power

    def apply_heat(self, power):
        self.temperature += power

    def switch(self, value):
        self.enabled = value

    def tick(self):
        self.rotation_speed -= 1
        self.rotation_speed = max(0, self.rotation_speed)
        self.temperature -= 1
        self.temperature = max(0, self.temperature)


class Crusher():
    def __init__(self):
        self.oil_level = 0
        self.enabled = False

    def add_oil(self, oil):
        self.oil_level += oil

    def switch(self, value):
        self.enabled = value

    def tick(self):
        self.oil_level -= 0.5
        self.oil_level = max(0, self.oil_level)


class Tank():
    def __init__(self):
        self.temperature = 0
        self.liquid_level = 0
        self.rotation_speed = 0
        self.enabled = False

    def apply_rotation_power(self, power):
        self.rotation_speed += power

    def add_liquid(self, liquid):
        self.liquid_level += liquid

    def apply_heat(self, power):
        self.temperature += power

    def switch(self):
        self.enabled = not self.enabled

    def pump_out(self, value):
        self.liquid_level -= value

    def tick(self):
        self.rotation_speed -= 1
        self.rotation_speed = max(0, self.rotation_speed)
        self.temperature -= 1
        self.temperature = max(0, self.temperature)
        self.liquid_level -= 1
        self.liquid_level = max(0, self.liquid_level)
