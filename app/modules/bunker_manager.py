from db import get_session
from sqlmodel import select, text, Session
import models
from typing import List, Optional
from utils.events.event_bus import EventBus
import datetime
from modules.process_management import get_current_process_id
from typing import List


# --- Обработчики входящих сигналов
def add_load_point(load_dt, bunker_id, quantity, type, source_bunker_id, session=next(get_session())):
    process_id = get_current_process_id()
    load = models.AluminaLoadModel(
        load_dt=load_dt,
        bunker_id=bunker_id,
        type_id=type,
        quantity=quantity,
        process_id=process_id,
        source_bunker_id=source_bunker_id)

    session.add(load)
    session.commit()
    EventBus.invoke("bunkers_updated")


def add_feed_point(feed_dt, bunker_id, quantity, session=next(get_session())):
    process_id = get_current_process_id()
    feed = models.AluminaFeedModel(
        feed_dt=feed_dt,
        bunker_id=bunker_id,
        quantity=quantity,
        process_id=process_id)
    EventBus.invoke("bunkers_updated")
    source_id = get_source_bunker_id(bunker_id)
    if not source_id:
        return
    estimate_quantity(source_id)
    session.add(feed)
    session.commit()


def update_state(measure_dt, data, session=next(get_session())):
    process_id = get_current_process_id()
    for sensor in data:

        input_source_id = sensor["input_source_id"]
        value = sensor["value"]
        bunker = session.exec(
            select(models.BunkerModel).where(models.BunkerModel.input_source_id == input_source_id)
        ).first()
        if not bunker:
            return
        state = models.BunkerStateModel(
            measure_dt=measure_dt,
            bunker_id=bunker.bunker_id,
            quantity=value,
            is_estimate=False,
            process_id=process_id
        )
        session.add(state)
    session.commit()
    EventBus.invoke("bunkers_updated")


# --- Вспомогательные функции
def estimate_quantity(bunker_id, session=next(get_session())):
    process_id = get_current_process_id()
    last_load_time = get_last_load_time(bunker_id)
    if not last_load_time:
        return
    last_state = get_last_bunker_state(bunker_id, last_load_time)

    connected_aas = get_connected_aas(bunker_id)
    query_file = "../resources/get_feed_sum.sql"
    with open(f"resources/{query_file}") as query:
        query_str = query.read() \
            .replace(":connected_aas", str(",".join(connected_aas))) \
            .replace(":load_time", last_load_time.strftime("'%Y-%m-%d %H:%M:%S.%f'"))
        feed_sum = session.exec(
            text(query_str)
        ).all()
    if not feed_sum[0][0]:
        return
    new_state = models.BunkerStateModel(
        measure_dt=datetime.datetime.now(),
        bunker_id=bunker_id,
        quantity=last_state.quantity - feed_sum[0][0],
        is_estimate=True,
        process_id=process_id
    )
    session.add(new_state)
    session.commit()


def get_last_load_time(bunker_id):
    last_load = get_last_alumina_move("load", bunker_id)
    if last_load:
        return last_load.load_dt
    return None


def get_last_alumina_move(move_type, bunker_id=None, row_limit=1,
                          session=next(get_session())
                          ) -> models.AluminaLoadModel | \
                               models.AluminaFeedModel | \
                               List[models.AluminaLoadModel] | \
                               List[models.AluminaFeedModel]:
    process_id = get_current_process_id()
    model = models.AluminaFeedModel if move_type.upper() == "FEED" else models.AluminaLoadModel
    dttm_field = models.AluminaFeedModel.feed_dt if move_type.upper() == "FEED" else models.AluminaLoadModel.load_dt
    result = session.exec(
        select(model)
        .where(not bunker_id or model.bunker_id == bunker_id)
        .where(model.process_id == process_id)
        .order_by(dttm_field.desc())
        .limit(row_limit)
    ).all()
    if row_limit == 1 and len(result) > 0:
        return result[0]
    return result


def get_source_bunker_id(bunker_id, session=next(get_session())):
    return session.exec(
        select(models.AluminaLoadModel.source_bunker_id)
        .where(models.AluminaLoadModel.bunker_id == bunker_id)
        .order_by(models.AluminaLoadModel.load_dt.desc())
    ).first()


def get_connected_aas(source_id, session=next(get_session())):
    query_file = "../resources/get_connected_aas.sql"
    with open(f"resources/{query_file}") as query:
        query_str = query.read().replace(":source_id", str(source_id))
        rows = session.exec(
            text(query_str)
        ).all()
    return [str(x[0]) for x in rows]


# include_est - включать ли оценочные значения (0 - нет, 1-да, 2-только оценочные)
def get_bunkers_states(is_aas, include_est=0, session=next(get_session())):
    query_file = "../resources/get_last_bunker_states.sql"
    with open(f"resources/{query_file}") as query:
        query_str = query.read().replace(":is_aas", str(is_aas)).replace(":include_est", str(include_est))
        return session.exec(
            text(query_str)
        ).all()


def get_last_bunker_state(bunker_id: int,
                          until: Optional[datetime.datetime] = None,
                          include_est: Optional[int] = 0,
                          session: Optional[Session] = next(get_session())) -> Optional[models.BunkerStateModel]:
    process_id = get_current_process_id()
    query = select(models.BunkerStateModel) \
        .where(models.BunkerStateModel.bunker_id == bunker_id) \
        .where(models.BunkerStateModel.process_id == process_id)

    if include_est == 0:
        query = query.where(models.BunkerStateModel.is_estimate == False)
    if until:
        query = query.where(models.BunkerStateModel.measure_dt <= until + datetime.timedelta(seconds=1.1))
    return session.exec(query.order_by(models.BunkerStateModel.measure_dt.desc())).first()


def get_bunker(bunker_id, session=next(get_session())):
    return session.exec(
        select(models.BunkerModel)
        .where(models.BunkerModel.bunker_id == bunker_id)
    ).first()


def get_bunkers(aas=False, session=next(get_session())):
    return session.exec(
        select(models.BunkerModel)
        .where(models.BunkerModel.is_aas == aas)
    ).first()


# include_est - включать ли оценочные значения (0 - нет, 1-да, 2-только оценочные)
def get_quantity_info(bunker_id: int,
                      window_size: int,
                      include_est: Optional[int] = 0,
                      session: Optional[Session] = next(get_session())
                      ) -> List[models.BunkerStateModel]:
    process_id = get_current_process_id()
    query = select(models.BunkerStateModel) \
        .where(models.BunkerStateModel.bunker_id == bunker_id) \
        .where(models.BunkerStateModel.process_id == process_id) \
        .where(models.BunkerStateModel.is_estimate == (include_est == 2))

    return session.exec(query.order_by(models.BunkerStateModel.measure_dt.desc()).limit(window_size)).all()


EventBus.add_event("bunkers_updated")
EventBus.subscribe("alumina_load", add_load_point)
EventBus.subscribe("alumina_feed", add_feed_point)
EventBus.subscribe("input", update_state)
