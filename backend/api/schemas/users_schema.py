from pydantic import BaseModel as BaseConf, ConfigDict, EmailStr, Field, field_validator
from typing import List, Literal

class BaseModel(BaseConf):
  model_config = ConfigDict(from_attributes=True)


class CreateUser(BaseModel):
  first_name: str
  last_name: str | None
  email: EmailStr
  phone_number: int | None
  password: str

  @field_validator('first_name')
  def first_name_validation(cls, v) -> str:
    if not v.isalpha():
        raise ValueError('First name must contain only letters')
    return v


  @field_validator("email")
  @classmethod
  def validate_email(cls, email: str) -> str:
    if email and not email.endswith("@gmail.com"):
      raise ValueError("Email must be a @gmail.com address")
    return email



class GoogleAuth(BaseModel):
   ...


class LoginUser(BaseModel):
   email: EmailStr
   password: str

