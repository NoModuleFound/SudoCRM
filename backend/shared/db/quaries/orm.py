from ..database import async_engine
from ..models import *


class AsyncORM:

    @staticmethod
    async def create_db():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def drop_db():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


    @staticmethod
    async def setup_db():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            