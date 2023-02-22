from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

table_args = {
    "schema": "cnf",
    "extend_existing": True
}

class ConfigParameterModel(SQLModel, table=True):
    __tablename__ = "config_parameter"
    __table_args__ = table_args

    parameter_id: Optional[int] = Field(default=None, primary_key=True)
    parameter_name: str = Field(default="")

class ConfigurationModel(SQLModel, table=True):
    __tablename__ = "configuration"
    __table_args__ = table_args

    configuration_id: Optional[int] = Field(default=None, primary_key=True)
    parameter_id: int = Field(default=None, foreign_key="cnf.config_parameter.parameter_id", primary_key=True)
    parameter: Optional[ConfigParameterModel] = Relationship(sa_relationship="config_parameter")
    value: str = Field(default=None)





