from .event import Event
from typing import Dict
from modules.logger import info, warn


class EventBus:
    events: Dict[str, Event] = {}
    unhandled_subs = []

    @staticmethod
    def add_event(name):
        EventBus.events[name] = Event()
        info(f"Created event [{name}]")
        unhandle_match = list(filter(lambda x: x[0] == name, EventBus.unhandled_subs))
        if unhandle_match:
            for x in unhandle_match:
                EventBus.events[name].subscribe(x[1])
                info(f"Resolved unhandled subscription to event [{name}] with handler [{x[1].__name__}]")

    @staticmethod
    def subscribe(name, handler):
        if name not in EventBus.events:
            EventBus.unhandled_subs.append((name, handler))
            warn(f"Unhandled subscription to event [{name}] with handler [{handler.__name__}]")
            return
        EventBus.events[name].subscribe(handler)

    @staticmethod
    def invoke(name, **kwargs):
        EventBus.events[name].invoke(**kwargs)
        info(f"Invoked event [{name}]")
