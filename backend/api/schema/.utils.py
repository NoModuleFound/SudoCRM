from pydantic import BaseModel as BaseConfig, ConfigDict


class BaseModel(BaseConfig):

  model_config = ConfigDict(from_attributes=True)