from sqlmodel import SQLModel
from ..database import async_engine
from ..models import UserORM, CredentialORM, TelegramDataORM, OrganizationORM

class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    @staticmethod
    async def drop_database():
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)

    @staticmethod
    async def setup_db():
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
            await conn.run_sync(SQLModel.metadata.create_all)

