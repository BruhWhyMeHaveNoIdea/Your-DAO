from bot.db.models.admins import Admins
import bot.db.crud.admins as crud_admins


async def create_default_table():
    if (await crud_admins.get_admin("Walkerin")):
        return "botva"
    admin_model = Admins(
        user_nickname="Walkerin"
    )
    await crud_admins.create_admin(admin_model)
