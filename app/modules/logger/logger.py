from db import get_session
from models import LogsModel
from datetime import datetime

def log(description, session = next(get_session())):
    #print(description)
    # log = LogsModel(
    #     log_dt=datetime.now(),
    #     description=description
    # )
    # session.add(log)
    # session.commit()
    pass