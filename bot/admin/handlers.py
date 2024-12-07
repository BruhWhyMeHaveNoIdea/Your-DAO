from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

import bot.admin.texts as texts
import bot.admin.keyboards as keyboards
from bot.db.models.admins import Admins
from bot.db.models.banned_users import Banned
from bot.bot import bot

import bot.db.crud.users as crud_users
import bot.db.crud.admins as crud_admins
import bot.db.crud.banned_users as crud_banned

router = Router()


@router.message(Command("admin"))
async def admin_command(message: Message, state: FSMContext):
    await state.clear()

    user_id = message.from_user.username
    if await crud_banned.read_banned(user_id):
        return
    if not await crud_admins.get_admin(user_id):
        return await message.answer(
            text=texts.not_access,
            reply_markup=keyboards.user_menu_keyboard
        )

    await message.answer(
        text=texts.yes_access,
        reply_markup=keyboards.admin_menu_keyboard
    )


@router.callback_query(F.data == "admin")
async def admin_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    user_id = callback.from_user.username

    if await crud_banned.read_banned(user_id):
        return

    if not crud_admins.get_admin(user_id):
        return await callback.message.answer(
            text=texts.not_access,
            reply_markup=keyboards.user_menu_keyboard
        )

    await callback.message.answer(
        text=texts.yes_access,
        reply_markup=keyboards.admin_menu_keyboard
    )


class UsersState(StatesGroup):
    add_user = State()
    ban_user = State()
    add_admin = State()
    delete_admin = State()
    send_newsletter = State()


@router.callback_query(F.data == "add_user")
async def add_user_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()
    await state.clear()
    await callback.message.answer(
        text=texts.add_user_text
    )
    await state.set_state(UsersState.add_user)
    await state.update_data({"type": "username"})


@router.message(UsersState.add_user)
async def add_admin(message: Message, state: FSMContext):
    msg = message.text
    if (await state.get_data())["type"] == "username":
        await state.update_data({"nickname": msg})
        await message.answer(
            text="А теперь введите, какой тип подписки вы хотите ему выдать (1 - Без доступа к GPT, но с доступом ко всему остальному; 2 - Полный доступ)")
        await state.update_data({'type': 'subscription'})
    elif (await state.get_data())["type"] == "subscription":
        try:
            msg = int(msg)
        except:
            return await message.answer(text="Введено не число")
        if msg not in range(1, 3):
            return await message.answer(text="Введено не правильное число")
        nickname, subs = (await state.get_data())["nickname"], msg
        await crud_users.update_user(nickname, "subscription_type", subs)
        await state.clear()
        await message.answer(text="Успешно!")
    else:
        print('Something Went Wrong')


@router.callback_query(F.data == "ban_user")
async def ban_user(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text="Отправьте никнейм пользователя, которого необходимо заблокировать")
    await state.set_state(UsersState.ban_user)


@router.message(UsersState.ban_user)
async def ban_user(message: Message, state: FSMContext):
    msg = message.text
    await state.clear()
    query = Banned(
        user_nickname=msg
    )
    await crud_banned.create_banned(query)
    await message.answer(text="Успешно забанен")


@router.callback_query(F.data == "add_admin")
async def add_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text="Введите никнейм пользователя")
    await state.set_state(UsersState.add_admin)


@router.message(UsersState.add_admin)
async def add_admin(message: Message, state: FSMContext):
    msg = message.text
    await state.clear()
    query = Admins(
        user_nickname=msg
    )
    await crud_admins.create_admin(query)
    await message.answer(text="Успешно!")


@router.callback_query(F.data == "delete_admin")
async def delete_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text="Введите никнейм пользователя")
    await state.set_state(UsersState.delete_admin)


@router.message(UsersState.delete_admin)
async def delete_admin(message: Message, state: FSMContext):
    msg = message.text
    await state.clear()
    try:
        await crud_admins.delete_admin(msg)
    except:
        return await message.answer(text="Админ не найден")
    await message.answer(text="Успешно!")


@router.callback_query(F.data == 'send_newsletter')
async def send_newsletter(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text="Введите сообщение")
    await state.set_state(UsersState.send_newsletter)


@router.message(UsersState.send_newsletter)
async def send_newsletter(message: Message, state: FSMContext):
    await state.clear()
    users = await crud_users.get_all_users()
    for i in users:
        i = i[0]
        try:
            await bot.copy_message(
                chat_id=i,
                from_chat_id=message.from_user.id,
                message_id=message.message_id
            )
        except Exception as e:
            print(e)
            print(f"user {i[0]} banned bot")
    await message.answer(text="Успешно!")
