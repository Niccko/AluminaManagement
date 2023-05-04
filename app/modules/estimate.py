import datetime
import json

from modules.configuration.config import get_active_config
import modules.bunker_manager as bunker_manager
import statistics
from db import get_session
from sqlmodel import select, text
from models import AluminaFeedModel, BunkerStateModel
from utils.events.event_bus import EventBus
import modules.configuration as config
import os
from modules.tcp.tcp_server import get_hardware_client

load_queue = []


def estimate_value(est_point, rates, value):
    mean_rate = statistics.mean(rates)
    return -(value - est_point) / mean_rate


# def est_devastation(session=next(get_session()), **kwargs):
#     config = get_active_config()
#     bunker_id = kwargs.get("bunker_id")
#     wind_size = int(config.get("derivative_win_size"))
#
#     quantity = session.exec(
#         select(BunkerStateModel)
#         .where(BunkerStateModel.bunker_id == bunker_id)
#         .order_by(BunkerStateModel.measure_dt.desc())
#     ).first()
#
#     feeds = session.exec(
#         select(AluminaFeedModel)
#         .where(AluminaFeedModel.bunker_id == bunker_id)
#         .where(AluminaFeedModel.feed_dt > quantity.measure_dt - datetime.timedelta(seconds=wind_size))
#         .order_by(AluminaFeedModel.feed_dt.desc())
#     ).all()
#     if not feeds:
#         return 0
#     feed_dt_window = (quantity.measure_dt - feeds[-1].feed_dt).total_seconds()
#     feeds = [feed.quantity for feed in feeds]
#     if feed_dt_window > 0:
#         return quantity.quantity / (sum(feeds) / feed_dt_window)
#     return 0

def est_devastation(session=next(get_session()), **kwargs):
    bunker_id = kwargs.get("bunker_id")
    last_load = bunker_manager.get_last_load_time(bunker_id)
    quantity = session.exec(
        select(BunkerStateModel)
        .where(BunkerStateModel.bunker_id == bunker_id)
        .where(last_load and BunkerStateModel.measure_dt > last_load)
        .order_by(BunkerStateModel.measure_dt.desc())
    ).all()
    if not quantity:
        return None
    times = [q.measure_dt.timestamp() for q in quantity]
    quantities = [q.quantity for q in quantity]
    mean_time = statistics.mean(times)
    mean_quantity = statistics.mean(quantities)
    num = 0
    denum = 0
    for i, t in enumerate(times):
        num += (t - mean_time) * (quantities[i] - mean_quantity)
        denum += (t - mean_time) * (t - mean_time)
    if num == 0 or denum == 0:
        return None
    a = num / denum
    b = mean_quantity - a * mean_time
    return -b / a - times[0]


# def est_devastation_all(session=next(get_session())):
#     query_file = "../resources/mean_square.sql"
#     with open(f"resources/{query_file}") as query:
#         query_str = query.read()
#         rows = session.exec(
#             text(query_str)
#         ).all()
#     return rows

def est_devastation_all():
    bunkers = bunker_manager.get_bunkers()
    res = []
    for bunker in bunkers:
        res.append({
            "bunker_id": bunker.bunker_id,
            "rem_time": est_devastation(bunker_id=bunker.bunker_id)
        })
    return res


def check_devastation():
    global load_queue
    rem = est_devastation_all()
    res = [
        x for x in rem if
        x.get("rem_time")
        and x.get("rem_time") < float(config.get("critical_time_threshold"))
        and bunker_manager.get_last_bunker_state(x.get("bunker_id")).quantity < float(
            config.get("soft_critical_quantity"))
    ]

    incr = [x for x in res if x.get("bunker_id") not in map(lambda y: y.get("bunker_id"), load_queue)]
    load_queue = sorted(res, key=lambda x: x.get("rem_time"))
    for r in incr:
        msg = {
            "event_type": "aas_load",
            "data": {
                "bunker_id": r.get("bunker_id"),
                "source_silage_id": bunker_manager.get_source_bunker_id(r.get("bunker_id")),
                "remaining_time": r.get("rem_time"),

            }
        }
        msg = json.dumps(msg) + "#"
        get_hardware_client().sendall(msg.encode("utf-8"))
    return load_queue

