import models
from models import *
from db import get_session
from datetime import datetime
from utils import EventBus
from sqlmodel import delete, exists, select
from modules.logger import warn

process_id = None

load_queue = []


def get_load_queue():
    return load_queue


def set_load_queue(queue):
    global load_queue
    load_queue = queue


def start_process(session=next(get_session())):
    global process_id
    process = ProcessModel(start_dttm=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    session.add(process)
    session.commit()
    session.refresh(process)
    process_id = process.process_id


def get_current_process_id():
    return process_id


def get_current_process(session=next(get_session())):
    return session.exec(
        select(ProcessModel).where(ProcessModel.process_id == process_id)
    ).first()


def topology_updated(topology, session=next(get_session())):
    warn("Comparing topology")
    bunker_count = len(session.exec(select(BunkerModel)).all())
    sensor_count = len(session.exec(select(InputSource)).all())
    if bunker_count != len(topology.get("sensors")) or sensor_count != len(topology.get("bunkers")):
        return True
    for sensor in topology.get("sensors"):
        sensor_exist = session.exec(
            exists(select(InputSource)
                   .where(InputSource.input_source_id == sensor["input_source_id"])
                   .where(InputSource.data_type == sensor["data_type"])
                   .where(InputSource.input_name == sensor["input_name"])).select()
        ).first()[0]
        if not sensor_exist:
            return True
    for bunker in topology.get("bunkers"):
        bunker_exist = session.exec(
            exists(select(BunkerModel)
                   .where(BunkerModel.bunker_id == bunker["bunker_id"])
                   .where(BunkerModel.is_aas == bunker["is_aas"])
                   .where(BunkerModel.capacity == bunker["capacity"])
                   .where(BunkerModel.input_source_id == bunker["input_source_id"])).select()
        ).first()[0]
        if not bunker_exist:
            return True
    warn("Topology did not changed")
    return False


def init_topology(data, session=next(get_session())):
    if not topology_updated(data):
        return
    warn(f"Updating topology: {data}")

    for sensor in data.get("sensors"):
        if not session.get(models.InputSource, sensor["input_source_id"]):
            session.add(InputSource(
                input_source_id=sensor["input_source_id"],
                data_type=sensor["data_type"],
                input_name=sensor["input_name"]
            ))
    session.commit()
    for bunker in data.get("bunkers"):
        b = session.get(models.BunkerModel, bunker["bunker_id"])
        if b:
            b.capacity = bunker["capacity"]
            b.is_aas = bunker["is_aas"]
            b.input_source_id = bunker["input_source_id"]
            b.deleted_flg = False

            warn(f"Updated bunker {b.bunker_id}")
        else:
            b = models.BunkerModel(
                bunker_id=bunker["bunker_id"],
                capacity=bunker["capacity"],
                is_aas=bunker["is_aas"],
                input_source_id=bunker["input_source_id"],
                deleted_flg=False
            )
        session.add(b)
    deleted = session.exec(select(models.BunkerModel)).all()
    top_ids = list([x["bunker_id"] for x in data.get("bunkers")])
    deleted = [y for y in deleted if y.bunker_id not in top_ids]
    for d in deleted:
        d.deleted_flg = True
        session.add(d)
        warn(f"Deleted bunker {d.bunker_id}")
    session.commit()
    warn("Topology updated")


EventBus.subscribe("process_start", start_process)
EventBus.subscribe("init_topology", init_topology)
