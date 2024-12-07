from bot.db.db import engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, delete, update
from bot.db.models.banned_users import Banned
from bot.db.schemas.banned_users import Banned as BannedDB


async def create_banned(user: Banned):
    async with AsyncSession(engine) as session:
        banned_db = BannedDB(
            user_nickname=user.user_nickname
        )
        session.add(banned_db)
        await session.commit()
        # return admin_db.id


async def read_banned(user_id: str):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(BannedDB).where(BannedDB.user_nickname == user_id)
        )
        query = result.scalars().first()
        return query is not None


async def remove_banned(user_id: str):
    async with AsyncSession(engine) as session:
        await session.execute(delete(BannedDB).where(BannedDB.user_nickname == user_id))
        await session.commit()