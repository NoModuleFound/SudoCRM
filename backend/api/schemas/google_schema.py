from pydantic import BaseModel as BaseConf, ConfigDict, EmailStr, Field, field_validator
from typing import List, Literal

class BaseModel(BaseConf):
  model_config = ConfigDict(from_attributes=True)

RowTypeEnum = Literal['integer_value', 'float_value', 'string_value', 'date_value', 'time_value', 'enum_value']

class RowSchema(BaseModel):
  header: str = Field(..., description="Header of column")
  row_type: RowTypeEnum = Field(..., description="Type data of column")

class SheetDataSchema(BaseModel):
  sheet_id: str = Field(..., description="ID Google Sheet")
  sheet_name: str = Field(..., description="Title")
  rows: List[RowSchema] = Field(..., description="Data of column")

class CreateSheetSchema(BaseModel):
  title: str = Field(..., description="Название таблицы")
  email: EmailStr | None = Field(None, description="Gmail-адрес пользователя")
  sheet_names: List = Field(..., description="Titles of sheets")

  @field_validator("email")
  @classmethod
  def validate_email(cls, email: str) -> str:
    if email and not email.endswith("@gmail.com"):
      raise ValueError("Email must be a @gmail.com address")
    return email

class RowDataSchema(BaseModel):
    sheet_id: str = Field(..., description="ID Google Sheet")
    sheet_name: str = Field(..., description="Sheet name")
    data: dict[str, str] = Field(..., description="Data mapped to headers {header: value}")
