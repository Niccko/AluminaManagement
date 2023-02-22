from db import get_session
from sqlmodel import Session, select, insert
import models
from utils.events.event_bus import EventBus
import datetime
import math
from modules.logger.logger import log

#TODO Порефакторить бы
class BunkerManager:
    def __init__(self) -> None:
        EventBus.subscribe("tcp_ready", self.start)

    def start(self):
        EventBus.subscribe("alumina_load", self.add_load_point)
        EventBus.subscribe("alumina_feed", self.add_feed_point)

    def add_load_point(self, bunker_id, quantity, type, session=next(get_session())):
        dt = datetime.datetime.now()
        load = models.AluminaLoadModel(
            load_dt=dt,
            bunker_id=bunker_id,
            type_id=type,
            quantity=quantity)

        last_state = self.get_last_bunker_state(bunker_id=bunker_id)
        new_state_quantity = last_state.quantity + quantity if last_state else quantity
        state = models.BunkerStateModel(
            measure_dt=dt,
            quantity=new_state_quantity,
            bunker_id=bunker_id,
            is_estimate=True
        )
        session.add(load)
        session.add(state)
        session.commit()

    def add_feed_point(self, bunker_id, quantity, session=next(get_session())):
        dt = datetime.datetime.now()
        feed = models.AluminaFeedModel(feed_dt=dt,
                                       bunker_id=bunker_id,
                                       quantity=quantity)
        last_state = self.get_last_bunker_state(bunker_id=bunker_id)
        new_state_quantity = last_state.quantity - quantity if last_state else 0
        if new_state_quantity <= 0:
            new_state_quantity = 0
            log(f"[WARNING] Bunker {bunker_id} is empty")
        state = models.BunkerStateModel(
            measure_dt=dt,
            quantity=new_state_quantity,
            bunker_id=bunker_id,
            is_estimate=True
        )
        session.add(feed)
        session.add(state)
        session.commit()

    def get_last_bunker_state(self, bunker_id, session=next(get_session())):
        return session.exec(
            select(models.BunkerStateModel)
            .where(models.BunkerStateModel.bunker_id == bunker_id)
            .order_by(models.BunkerStateModel.measure_dt.desc())
        ).first()

    def get_bunker_states(self, session=next(get_session())):
        with open("app\\modules\\bunker_management\\get_last_states.sql", "r+") as f:
            res = session.exec(f.read()).all()
            return res
        
