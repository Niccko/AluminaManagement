from db import get_session
from sqlmodel import Session, select, insert, func, text
import models
from utils.events.event_bus import EventBus
import datetime
from modules.logger.logger import log
from modules.configuration.config import get_active_config


# TODO Порефакторить бы


class BunkerManager:
    def __init__(self) -> None:
        EventBus.subscribe("tcp_ready", self.start)
        EventBus.add_event("bunkers_updated")

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
        session.add(load)
        session.commit()
        EventBus.invoke("bunkers_updated")

    def add_feed_point(self, bunker_id, quantity, session=next(get_session())):
        dt = datetime.datetime.now()
        feed = models.AluminaFeedModel(feed_dt=dt,
                                       bunker_id=bunker_id,
                                       quantity=quantity)
        session.add(feed)
        session.commit()
        EventBus.invoke("bunkers_updated")

    def get_last_bunker_state(self, bunker_id, session=next(get_session())):
        return session.exec(
            select(models.BunkerStateModel)
            .where(models.BunkerStateModel.bunker_id == bunker_id)
            .order_by(models.BunkerStateModel.measure_dt.desc())
        ).first()

    def get_aas_states(self, session=next(get_session())):
        with open("resources/get_last_aas_states.sql") as query:
            return session.exec(
                text(query.read())
            ).all()

    def get_bunkers_states(self, session=next(get_session())):
        with open("resources/get_last_bunker_states.sql") as query:
            return session.exec(
                text(query.read())
            ).all()

    def get_bunker(self, bunker_id, session=next(get_session())):
        return session.exec(
            select(models.BunkerModel)
            .where(models.BunkerModel.bunker_id == bunker_id)
        ).first()

    def get_quantity_info(self, bunker_id, session=next(get_session())):
        config = get_active_config()
        source_id = session.exec(select(models.BunkerModel.input_source_id)
                                 .where(models.BunkerModel.bunker_id == bunker_id)).first()
        return session.exec(
            select(models.Input)
            .where(models.Input.input_source_id == source_id)
            .order_by(models.Input.measure_dt.desc())
            .limit(config.get("qnt_show_window"))
        ).all()
