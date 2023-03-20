from db import get_session
from models import InputSource, Input
from datetime import datetime
from utils.events.event_bus import EventBus


def add_input_value(input_source_id, value, session=next(get_session())):
    inp = Input(
        measure_dt=datetime.now(),
        input_source_id=input_source_id,
        value=value
    )
    session.add(inp)
    session.commit()
    EventBus.invoke("bunkers_updated")


EventBus.subscribe("input", add_input_value)
