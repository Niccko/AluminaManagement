from sqlmodel import SQLModel, Field, ForeignKey, Relationship
from typing import Optional
import sqlalchemy as sa
import datetime

table_args = {
    "schema": "ddl",
    "extend_existing": True
}

class BunkerModel(SQLModel, table=True):
    __tablename__ = "bunker"
    __table_args__ = table_args

    bunker_id: Optional[int] = Field(default=None, primary_key=True)
    is_aas: bool = Field(default=True)
    capacity: float = Field(default=0)

class BunkerStateModel(SQLModel, table=True):
    __tablename__ = "bunker_state"
    __table_args__ = table_args

    measure_dt: datetime.datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, primary_key=True))
    bunker_id: int = Field(foreign_key="ddl.bunker.bunker_id", primary_key=True)
    quantity: float = Field(default=0)
    is_estimate: bool = Field(default=False)

class AluminaTypeModel(SQLModel, table=True):
    __tablename__ = "alumina_type"
    __table_args__ = table_args

    type_id: Optional[int] = Field(default=None, primary_key=True)
    provider_address: Optional[str] = Field(default=None)

class AluminaLoadModel(SQLModel, table=True):
    __tablename__ = "alumina_load"
    __table_args__ = table_args

    load_dt: datetime.datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False , primary_key=True))
    bunker_id: int = Field(foreign_key="ddl.bunker.bunker_id", primary_key=True)
    type_id: int = Field(foreign_key="ddl.alumina_type.type_id", primary_key=True)
    quantity: float = Field(default=True)

class AluminaFeedModel(SQLModel, table=True):
    __tablename__ = "alumina_feed"
    __table_args__ = table_args

    feed_dt: datetime.datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, primary_key=True))
    bunker_id: int = Field(foreign_key="ddl.bunker.bunker_id", primary_key=True)
    quantity: float = Field(default=True)

class LogsModel(SQLModel, table=True):
    __tablename__ = "logs"
    __table_args__ = table_args
    log_dt: datetime.datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, primary_key=True))
    description: Optional[str] = Field(default=None)