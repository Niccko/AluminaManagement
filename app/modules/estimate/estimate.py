from modules.configuration.config import get_config
import statistics
from db import get_session
from sqlmodel import select
from models import AluminaFeedModel, BunkerStateModel
from utils.events.event_bus import EventBus
import os


def estimate_value(est_point, rates, value):
    mean_rate = statistics.mean(rates)
    return -(value-est_point)/mean_rate


def est_devastation(session=next(get_session()), **kwargs):
    bunker_id = kwargs.get("bunker_id")
    config = get_config(1)
    wind_size = config.get("window_size")
    feeds = session.exec(
        select(AluminaFeedModel.quantity)
        .where(AluminaFeedModel.bunker_id == bunker_id)
        .order_by(AluminaFeedModel.feed_dt)
        .limit(wind_size)
    ).all()
    quantity = session.exec(
        select(BunkerStateModel)
        .where(BunkerStateModel.bunker_id == bunker_id)
        .order_by(BunkerStateModel.measure_dt.desc())
    ).first().quantity
    os.system('cls')
    print(estimate_value(quantity, feeds, 0))


EventBus.subscribe("alumina_feed", est_devastation)
