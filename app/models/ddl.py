from sqlmodel import SQLModel, Field, ForeignKey, Relationship
from typing import Optional
import sqlalchemy as sa
import datetime

table_args = {
    "schema": "ddl",
    "extend_existing": True
}


class ProcessModel(SQLModel, table=True):
    __tablename__ = "process"
    __table_args__ = table_args
    process_id: Optional[int] = Field(default=None, primary_key=True)
    start_dttm: datetime.datetime = Field(
        sa_column=sa.Column(sa.DateTime(timezone=True),
                            nullable=False)
    )


class InputSource(SQLModel, table=True):
    __tablename__ = "input_source"
    __table_args__ = table_args
    input_source_id: Optional[int] = Field(default=None, primary_key=True)
    data_type: Optional[str] = Field(default=None)
    input_name: Optional[str] = Field(default=None)


class BunkerModel(SQLModel, table=True):
    __tablename__ = "bunker"
    __table_args__ = table_args

    bunker_id: Optional[int] = Field(default=None, primary_key=True)
    is_aas: bool = Field(default=True)
    capacity: float = Field(default=0)
    input_source_id: int = Field(foreign_key="ddl.input_source.input_source_id")
    input_source: InputSource = Relationship()


class BunkerStateModel(SQLModel, table=True):
    __tablename__ = "bunker_state"
    __table_args__ = table_args

    measure_dt: datetime.datetime = Field(
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, primary_key=True))
    bunker_id: int = Field(foreign_key="ddl.bunker.bunker_id", primary_key=True)
    quantity: float = Field(default=0)
    is_estimate: bool = Field(default=False)
    process_id: int = Field(foreign_key="ddl.process.process_id")


class AluminaTypeModel(SQLModel, table=True):
    __tablename__ = "alumina_type"
    __table_args__ = table_args

    type_id: Optional[int] = Field(default=None, primary_key=True)
    provider_address: Optional[str] = Field(default=None)


class AluminaLoadModel(SQLModel, table=True):
    __tablename__ = "alumina_load"
    __table_args__ = table_args

    load_id: Optional[int] = Field(default=None, primary_key=True)
    load_dt: datetime.datetime = Field(
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False))
    bunker_id: int = Field(foreign_key="ddl.bunker.bunker_id")
    type_id: int = Field(foreign_key="ddl.alumina_type.type_id")
    quantity: float = Field(default=True)
    source_bunker_id: int = Field(foreign_key="ddl.bunker.bunker_id", nullable=True)
    process_id: int = Field(foreign_key="ddl.process.process_id")


class AluminaFeedModel(SQLModel, table=True):
    __tablename__ = "alumina_feed"
    __table_args__ = table_args

    feed_id: Optional[int] = Field(default=None, primary_key=True)
    feed_dt: datetime.datetime = Field(
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False))
    bunker_id: int = Field(foreign_key="ddl.bunker.bunker_id")
    quantity: float = Field(default=True)
    process_id: int = Field(foreign_key="ddl.process.process_id")


class LogsModel(SQLModel, table=True):
    __tablename__ = "logs"
    __table_args__ = table_args
    log_dt: datetime.datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, primary_key=True))
    log_type: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
