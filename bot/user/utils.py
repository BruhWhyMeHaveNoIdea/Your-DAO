import datetime

import httpx
import re
import bot.db.crud.users as crud_users


async def get_short_url(first_url):
    async with httpx.AsyncClient() as client:
        response = await client.get(first_url)
        if response.status_code == 200:
            match = re.search(r'https://payform.ru/[^\s"]+', response.text)
            if match:
                return match.group(0)
    return None


def recieve_num(theme, type):
    if type == 1:
        ar = ['people_games', 'contact_with_yourself', 'birth_programs', 'life_on']
        return ar.index(theme)+1
    else:
        ar = ['people_games', 'contact_with_yourself', 'birth_programs', 'life_on']
        return ar[theme]

async def delete_one_day():
    users = list(map(int, await crud_users.get_all_subscribers()))
    for i in users:
        user_day = await crud_users.get_user_days(i)
        if user_day > 0:
            user_day-=1
            await crud_users.update_user(i, 'sub_days', user_day)
        else:
            await crud_users.update_user(i, 'subscription_type', 0)

async def free_trial(user_id: int):
    if await crud_users.get_reg_date(user_id) is not None:
        left_time = (await crud_users.get_reg_date(user_id)) + datetime.timedelta(hours=24)
    else:
        return False
    sub_type = await crud_users.get_subscription_type(user_id)
    now = datetime.datetime.now(tz=datetime.UTC)
    if (left_time < now) and (sub_type == 0):
        return True
    return False
