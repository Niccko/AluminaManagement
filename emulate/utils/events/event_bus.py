from .event import Event
from typing import Dict


class EventBus:
    events: Dict[str, Event] = {}
    unhandled_subs = []

    @staticmethod
    def add_event(name):
        EventBus.events[name] = Event()
        unhandled_match = list(filter(lambda x: x[0] == name, EventBus.unhandled_subs))
        if unhandled_match:
            for x in unhandled_match:
                EventBus.events[name].subscribe(x[1])

    @staticmethod
    def subscribe(name, handler):
        if name not in EventBus.events:
            EventBus.unhandled_subs.append((name, handler))
            return
        EventBus.events[name].subscribe(handler)

    @staticmethod
    def invoke(name, **kwargs):
        EventBus.events[name].invoke(**kwargs)
