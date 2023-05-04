import models
from db import get_session
from models import LogsModel
from datetime import datetime
from sqlmodel import select

save_logs = True
show_info = False


def info(description):
    log("INFO", description)


def warn(description):
    log("WARNING", description)


def error(description):
    log("ERROR", description)


def log(log_type, message, session=next(get_session())):
    if not show_info and log_type == "INFO":
        return
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{time}] {log_type.upper()} - {message}")
    if not save_logs:
        return
    log_obj = LogsModel(
        log_dt=datetime.now(),
        log_type=log_type,
        description=message
    )
    session.add(log_obj)
    session.commit()


def get_logs(date_start, date_end, include, session=next(get_session())):
    print(include)
    query = select(models.LogsModel) \
        .where(models.LogsModel.log_dt > date_start) \
        .where(models.LogsModel.log_dt < date_end) \
        .where(models.LogsModel.log_type.in_(include)) \
        .order_by(models.LogsModel.log_dt.desc())
    return session.exec(query).all()
