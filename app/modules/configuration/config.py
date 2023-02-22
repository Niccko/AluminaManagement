from db import get_session
from sqlmodel import select
import models

config = None


def add_parameter(name, session = next(get_session())):
    session.add(models.ConfigParameterModel(parameter_name=name))
    session.commit()


def create_configuration(params: dict, session = next(get_session())):
    statement = select(models.ConfigParameterModel).distinct()
    res = session.exec(statement).all()
    parameter_list = [i.parameter_name for i in res]
    if set(parameter_list) != set(params):
        raise Exception("Parameters list must match " + str(parameter_list))

    conf_ids = session.exec(select(models.ConfigurationModel.configuration_id)).all()
    conf_id = 1 if not conf_ids else max(conf_ids) + 1
    for i in res:
        session.add(models.ConfigurationModel(configuration_id=conf_id,
                                              parameter_id=i.parameter_id,
                                              value=params[i.parameter_name]))
    session.commit()

def get_config(id, session = next(get_session())):
    global config
    if config:
        return config
    res = session.exec(select(models.ConfigurationModel, models.ConfigParameterModel)
    .where(models.ConfigurationModel.configuration_id == id)
    .join(models.ConfigParameterModel)).all()

    config = {}
    for i in res:
        config[i[1].parameter_name] = i[0].value
    return config


