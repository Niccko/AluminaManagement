import datetime

from modules.configuration.config import get_active_config
import statistics
from db import get_session
from sqlmodel import select, func
from models import AluminaFeedModel, BunkerStateModel
from utils.events.event_bus import EventBus
import os


def estimate_value(est_point, rates, value):
    mean_rate = statistics.mean(rates)
    return -(value - est_point) / mean_rate


def est_devastation(session=next(get_session()), **kwargs):
    config = get_active_config()
    bunker_id = kwargs.get("bunker_id")
    wind_size = int(config.get("derivative_win_size"))

    quantity = session.exec(
        select(BunkerStateModel)
        .where(BunkerStateModel.bunker_id == bunker_id)
        .order_by(BunkerStateModel.measure_dt.desc())
    ).first()

    feeds = session.exec(
        select(AluminaFeedModel)
        .where(AluminaFeedModel.bunker_id == bunker_id)
        .where(AluminaFeedModel.feed_dt > quantity.measure_dt - datetime.timedelta(seconds=wind_size))
        .order_by(AluminaFeedModel.feed_dt.desc())
    ).all()
    if not feeds:
        return 0
    feed_dt_window = (quantity.measure_dt - feeds[-1].feed_dt).total_seconds()
    feeds = [feed.quantity for feed in feeds]
    if feed_dt_window > 0:
        return quantity.quantity / (sum(feeds) / feed_dt_window)
    return 0
