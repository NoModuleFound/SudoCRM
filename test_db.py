from backend.shared.db.quaries.orm import AsyncORM
import asyncio

asyncio.run(AsyncORM.create_db())