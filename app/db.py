import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, Session
from models import *
from dotenv import load_dotenv
import global_vars

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
Base = declarative_base()
engine = create_engine(DATABASE_URL, pool_size=100)
global_vars.db_connected = True


def create_schema(conn, name):
    if name in conn.dialect.get_schema_names(conn):
        return
    conn.execute(CreateSchema(name))


def to_dict(self) -> dict:
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


def get_session():
    global sess
    try:
        session = Session(bind=engine)
        yield session
    finally:
        session.close()


# with engine.connect() as connection:
#     create_schema(connection, "cnf")
#     create_schema(connection, "ddl")
#     create_schema(connection, "rep")
#     connection.commit()
SQLModel.metadata.create_all(engine)
sess = sessionmaker(bind=engine)

SQLModel.to_dict = to_dict
metadata = SQLModel.metadata
