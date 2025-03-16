from pydantic import BaseModel as BaseConf, ConfigDict, EmailStr, Field, field_validator
from typing import Optional, Dict


class BaseModel(BaseConf):
  model_config = ConfigDict(from_attributes=True)


class ApiResponse(BaseModel):
    status_code: int
    message: str
    detail: Optional[Dict[str, str]] = None 