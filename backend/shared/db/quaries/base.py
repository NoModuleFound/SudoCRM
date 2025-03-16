from typing import Annotated
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from backend.shared.utils.misc import current_time


from sqlalchemy import (
    CheckConstraint, Column, Enum,
    ForeignKey, Index, Integer, MetaData, 
    PrimaryKeyConstraint, String, Table, text
)



intpk = Annotated[int, mapped_column(primary_key=True)]
time_now = Annotated[str, mapped_column(default=current_time())]

str_32 = Annotated[str, 32]
str_128 = Annotated[str, 128]
str_512 = Annotated[str, 512]
str_1028 = Annotated[str, 1029]



class Base(DeclarativeBase):

  annotation_mapping = {
    str_32: String(32),
    str_128: String(128),
    str_512: String(512),
    str_1028: String(1028)
  }