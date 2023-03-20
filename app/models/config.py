from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

table_args = {
    "schema": "cnf",
    "extend_existing": True
}


class ConfigXParams(SQLModel, table=True):
    __tablename__ = "config_x_params"
    __table_args__ = table_args
    parameter_id: int = Field(default=None, foreign_key="cnf.config_parameter.parameter_id", primary_key=True)
    configuration_id: int = Field(default=None, foreign_key="cnf.configuration.configuration_id", primary_key=True)
    value: str = Field(default=None)
    config: "ConfigurationModel" = Relationship(back_populates="params_links")
    param: "ConfigParameterModel" = Relationship(back_populates="config_links")


class ConfigParameterModel(SQLModel, table=True):
    __tablename__ = "config_parameter"
    __table_args__ = table_args

    parameter_id: Optional[int] = Field(default=None, primary_key=True)
    parameter_name: str = Field(default="")
    description: Optional[str] = Field(default="")
    type_name: Optional[str] = Field(default=None)
    config_links: List[ConfigXParams] = Relationship(back_populates="param")


class ConfigurationModel(SQLModel, table=True):
    __tablename__ = "configuration"
    __table_args__ = table_args

    configuration_id: Optional[int] = Field(default=None, primary_key=True)
    is_active: bool = Field(default=False)
    name: Optional[str] = Field(default=None)
    params_links: List[ConfigXParams] = Relationship(back_populates="config")
