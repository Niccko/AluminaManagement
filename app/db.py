import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, SQLModel, Session
from models import *
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = None
session = None

Base = declarative_base()


def to_dict(self) -> dict:
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


SQLModel.to_dict = to_dict
metadata = SQLModel.metadata
sess = None


def init_db():
    global engine, sess
    engine = create_engine(DATABASE_URL, echo=True)
    with engine.connect() as connection:
        create_schema(connection, "cnf")
        create_schema(connection, "ddl")
        create_schema(connection, "rep")
        connection.commit()
    SQLModel.metadata.create_all(engine)
    sess = sessionmaker(bind=engine)


def get_session():
    global sess
    try:
        session = Session(bind=engine)
        yield session
    finally:
        session.close()


def create_schema(connection, name):
    if name in connection.dialect.get_schema_names(connection):
        return
    connection.execute(CreateSchema(name))
