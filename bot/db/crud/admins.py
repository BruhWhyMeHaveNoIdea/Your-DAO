from bot.db.db import engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, delete, update
from bot.db.models.admins import Admins
from bot.db.schemas.admins import Admins as AdminsDB


async def create_admin(admin: Admins):
    async with AsyncSession(engine) as session:
        admin_db = AdminsDB(
            user_nickname=admin.user_nickname
        )
        session.add(admin_db)
        await session.commit()
        # return admin_db.id


async def read_admin(user_id: str):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(AdminsDB).where(AdminsDB.user_nickname == user_id)
        )
        query = result.scalars().first()
        return query


async def update_admin(user_id: str, new_user_id: str):
    async with AsyncSession(engine) as session:
        await session.execute(update(AdminsDB).where(AdminsDB.user_nickname == user_id).values(user_id=new_user_id))
        await session.commit()


async def delete_admin(user_id: str):
    async with AsyncSession(engine) as session:
        await session.execute(delete(AdminsDB).where(AdminsDB.user_nickname == user_id))
        await session.commit()


async def get_admin(user_id: str):
    admin = await read_admin(user_id)
    print(admin)
    return admin is not None
