from sqlalchemy import (ForeignKey, Enum, DateTime)
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime
from typing import List, Optional
from .quaries import (
    Base, intpk, time_now,
    str_32, str_128, str_512, str_1028)

from backend.shared.utils.misc import current_time

# from backend.api.schemas.book_schema import BookType, BookLang



class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    first_name: Mapped[str_32] = mapped_column(nullable=False)
    last_name: Mapped[str_32] = mapped_column(nullable=True)
    email: Mapped[str_32] = mapped_column(unique=True)
    password_hash: Mapped[bytes] = mapped_column(nullable=False)
    phone_number: Mapped[str_32] = mapped_column(unique=True, nullable=True)

    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[time_now]
    updated_at: Mapped[str] = mapped_column(onupdate=current_time(), nullable=True)


