from db import get_session
from sqlmodel import select
import models
from modules.configuration.utils import form_config

config = None


def create_configuration(params: dict, name=None, session=next(get_session())):
    statement = select(models.ConfigParameterModel).distinct()
    res = session.exec(statement).all()
    parameter_list = [i.parameter_name for i in res]
    if set(parameter_list) != set(params):
        raise Exception("Parameters list must match " + str(parameter_list))

    configuration = models.ConfigurationModel(is_active=False, name=name)
    session.add(configuration)
    session.flush()
    session.refresh(configuration)
    links = [models.ConfigXParams(
        configuration_id=configuration.configuration_id,
        parameter_id=param.parameter_id,
        value=params[param.parameter_name]
    ) for param in res]
    for i in links:
        session.add(i)
    session.commit()


def get_parameters(session=next(get_session())):
    statement = select(models.ConfigParameterModel).distinct()
    return session.exec(statement).all()


def get_config(config_id, session=next(get_session())):
    res = session.exec(select(models.ConfigurationModel)
                       .where(models.ConfigurationModel.configuration_id == config_id)
                       ).first()
    return form_config(res) if res else {}


def get_active_config(session=next(get_session())):
    res = session.exec(select(models.ConfigurationModel)
                       .where(models.ConfigurationModel.is_active)
                       ).first()

    return form_config(res) if res else {}


def get(param_name):
    global config
    if not config:
        config = get_active_config()
    return config.get(param_name)


def select_config(config_id, session=next(get_session())):
    global config
    for i in session.exec(select(models.ConfigurationModel)).all():
        i.is_active = i.configuration_id == config_id
    session.commit()
    config = get_active_config()


def delete_config(config_id, session=next(get_session())):
    res = session.exec(select(models.ConfigurationModel)
                       .where(models.ConfigurationModel.configuration_id == config_id)).all()
    for i in res:
        session.delete(i)
    session.commit()


def get_configs(session=next(get_session())):
    configs = session.exec(select(
        models.ConfigurationModel
    ).order_by(models.ConfigurationModel.configuration_id).distinct()).all()
    return configs
