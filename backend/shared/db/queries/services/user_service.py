from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload

# from backend.api.misc.auth_utils import *
from ...database import Base, async_engine, async_session_factory
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ...database import async_session_factory
from ...models import UserORM, CredentialORM




class UserManagement:
  ...