from db import get_session
from models import LogsModel
from datetime import datetime

def log(description, session = next(get_session())):
    log = LogsModel(
        log_dt=datetime.now(),
        description=description
    )
    session.add(log)
    session.commit()