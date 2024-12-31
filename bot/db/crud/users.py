from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, delete, update
from bot.db.db import engine
from bot.db.models.users import Users
from bot.db.schemas.users import Users as UsersDB
import pandas as pd
from datetime import timezone
import os


async def create_user(user: Users):
    async with AsyncSession(engine) as session:
        user_id = user.user_id
        if not(await read_user(user_id)):
            user_db = UsersDB(
                user_id=user.user_id,
                subscription_type=user.subscription_type,
                referral_users=user.referral_users,
                bonuses=user.bonuses,
                sub_days=user.sub_days,
                registration_date = user.registration_date
            )
            session.add(user_db)
            await session.commit()

async def get_all_users():
    async with AsyncSession(engine) as session:
        result = await session.execute(select(UsersDB.user_id))
        query = result.fetchall()
        return query


async def read_user(user_id: int):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(UsersDB).where(UsersDB.user_id == user_id)
        )
        query = result.scalars().first()
        return query


async def update_user(user_id: int, type: str, value:int):
    session = AsyncSession(engine)
    user_id = int(user_id)
    print(user_id, type, value)
    if type == "subscription_type":
        await session.execute(update(UsersDB).where(UsersDB.user_id == user_id).values(subscription_type=value))
    elif type == "referral_users":
        await session.execute(update(UsersDB).where(UsersDB.user_id == user_id).values(referral_users=value))
    elif type == "bonuses":
        await session.execute(update(UsersDB).where(UsersDB.user_id == user_id).values(bonuses=value))
    elif type == "sub_days":
        await session.execute(update(UsersDB).where(UsersDB.user_id == user_id).values(sub_days=value))
    else:
        await session.execute(update(UsersDB).where(UsersDB.user_id == user_id).values(active=value))
    await session.commit()


async def delete_user(user_id: int):
    async with AsyncSession(engine) as session:
        await session.execute(delete(UsersDB).where(UsersDB.user_id == user_id))
        await session.commit()

async def get_user(user_id: int):
    user = await read_user(user_id)
    if user is None:
        return False
    return True


async def update_bonuses(user_id: int, bonuses: int):
    async with AsyncSession(engine) as session:
        await session.execute(update(UsersDB).where(UsersDB.user_id == user_id).values(bonuses=bonuses))
        await session.commit()


async def update_referral_users(user_id: int, referral_users: int):
    async with AsyncSession(engine) as session:
        await session.execute(update(UsersDB).where(UsersDB.user_id == user_id).values(referral_users=referral_users))
        await session.commit()


async def get_subscription_type(user_id):
    user = await read_user(user_id)
    if user is None:
        return 0
    return user.subscription_type

async def get_all_subscribers():
    async with AsyncSession(engine) as session:
        result = await session.execute(select(UsersDB.user_id).where(UsersDB.subscription_type.in_([1,2])))
        query = [row[0] for row in result.fetchall()]
        return query

async def get_user_days(user_id: int):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(UsersDB.sub_days).where(UsersDB.user_id == user_id))
        query = result.scalars().first()
        return query

async def get_reg_date(user_id: int):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(UsersDB.registration_date).where(UsersDB.user_id == user_id))
        query = result.scalars().first()
        return query

async def return_excel():
    async with AsyncSession(engine) as session:
        current_dir = os.getcwd()
        project_dir = os.path.join(current_dir, "files")
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        sm = select(UsersDB.user_id,UsersDB.registration_date,UsersDB.sub_days,UsersDB.subscription_type)
        result = await session.execute(sm)
        users = result.all()
        df = pd.DataFrame([{"ID Пользователя": user.user_id,"Дата регистрации": user.registration_date.astimezone(timezone.utc).replace(tzinfo=None), "Осталось дней подписки": user.sub_days, "Тип подписки": "Полный доступ" if user.subscription_type == 2 else "Доступ к урокам"} for user in users])
        df.to_excel(excel_writer=os.path.join(project_dir,"Database.xlsx"), index=False)