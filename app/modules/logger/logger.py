from db import get_session
from models import LogsModel
from datetime import datetime

save_logs = False
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
        description=log_type
    )
    session.add(log_obj)
    session.commit()
