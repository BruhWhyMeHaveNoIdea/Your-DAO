import datetime

from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.types import InputMediaVideo, InputMediaDocument, InputMediaAudio
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.bot import bot

import bot.user.texts as texts
import bot.user.keyboards as keyboards
import bot.user.utils as utils
import bot.user.media as media
import config

from bot.db.models.users import Users
import bot.db.crud.users as crud_users
import bot.db.crud.banned_users as crud_banned
from bot.user.texts import presentations_file_ids

router = Router()


@router.message(Command('start'))
async def start_command(message: Message, state: FSMContext):
    await state.clear()

    user_id = (message.from_user.id)
    if (await crud_banned.read_banned(message.from_user.username)):
        return
    if not (await crud_users.get_user(user_id)):
        args = message.text.split()
        if len(args) != 1:
            from_user_id = int(args[-1])
            referral_user = await crud_users.read_user(from_user_id)

            new_bonuses = referral_user.bonuses + 1
            new_referral_users = referral_user.referral_users + 1

            await crud_users.update_bonuses(from_user_id, new_bonuses)
            await crud_users.update_referral_users(from_user_id, new_referral_users)

        user = Users(
            user_id=user_id,
            subscription_type=0,
            referral_users=0,
            bonuses=0,
            sub_days=0,
            active=False,
            registration_date=datetime.datetime.now(datetime.UTC)
        )
        await crud_users.create_user(user)
    await message.answer_photo(
        # test_video
        photo="AgACAgIAAxkBAAIEiGc6I2y9j89o1EbzMxpVQfTYyV0tAAK15TEbb2LRScBmF-RravqLAQADAgADcwADNgQ",
        caption=texts.start_text,
        reply_markup=keyboards.start_keyboard()
    )


@router.callback_query(F.data == "chat")
async def chat(callback: CallbackQuery):
    user_id = callback.from_user.id
    if await utils.free_trial(user_id):
        try:
            return await callback.message.edit_text(
                text=texts.no_left_time,
                reply_markup=keyboards.to_subscription_keyboard
            )
        except:
            return await callback.message.answer(
                text=texts.no_left_time,
                reply_markup=keyboards.to_subscription_keyboard
            )
    if (await crud_users.get_subscription_type(user_id)) == 0:
        try:
            return await callback.message.edit_text(
                text=texts.no_access_to_materials,
                reply_markup=keyboards.to_subscription_keyboard
            )
        except:
            return await callback.message.answer(
                text=texts.no_access_to_materials,
                reply_markup=keyboards.to_subscription_keyboard
            )
    await callback.answer()
    await callback.message.answer(text=f"Добро пожаловать! \n\n https://t.me/+BzP-5s1sMmE3ZDMy")


@router.callback_query(F.data == "start")
async def start_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    try:
        await callback.message.edit_reply_markup()
    except Exception as e:
        """went from message("""
        ...
    if await crud_banned.read_banned(callback.message.from_user.username):
        return
    await callback.message.answer_photo(
        # test_video
        photo="AgACAgIAAxkBAAIEiGc6I2y9j89o1EbzMxpVQfTYyV0tAAK15TEbb2LRScBmF-RravqLAQADAgADcwADNgQ",
        caption=texts.start_text,
        reply_markup=keyboards.start_keyboard()
    )


@router.callback_query(F.data == "video_materials")
async def video_materials_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    try:
        await callback.message.delete()
    except:
        ...
    if (await utils.free_trial(callback.from_user.id)):
        return await callback.message.answer(
            text=texts.no_left_time,
            reply_markup=keyboards.to_subscription_keyboard
        )
    await callback.message.answer(text=texts.video_materials_text,
                                      reply_markup=keyboards.video_materials_keyboard())


@router.callback_query(F.data == "people_games")
async def people_games(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.edit_text(text=texts.people_games, reply_markup=keyboards.people_games_theme())
    except:
        await callback.message.answer(text=texts.people_games, reply_markup=keyboards.people_games_theme())


@router.callback_query(F.data == "contact_with_yourself")
async def contact_with_yourself(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.edit_text(text=texts.contact_with_yourself,
                                         reply_markup=keyboards.contact_with_yourself())
    except:
        await callback.message.answer(text=texts.contact_with_yourself, reply_markup=keyboards.contact_with_yourself())


@router.callback_query(F.data == "birth_programs")
async def birth_programs(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.edit_text(text=texts.birth_programs, reply_markup=keyboards.birth_programs())
    except:
        await callback.message.answer(text=texts.birth_programs, reply_markup=keyboards.birth_programs())


@router.callback_query(F.data == "life_on")
async def life_on(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.edit_text(text=texts.life_on, reply_markup=keyboards.life_on())
    except:
        await callback.message.answer(text=texts.life_on, reply_markup=keyboards.life_on())


@router.callback_query(F.data.startswith("people_games_theme"))
async def people_games_theme(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.delete()
    except:
        ...
    theme = int(callback.data.split("_")[-1])
    if await utils.free_trial(callback.from_user.id):
        return await callback.message.answer(
            text=texts.no_left_time,
            reply_markup=keyboards.to_subscription_keyboard
        )
    if theme == 1:
        text = texts.video_materials_phrases[1][1]
        video = texts.video_file_ids[1][1]
        return await callback.message.answer_video(video=video, caption=text,
                                                   reply_markup=keyboards.themes_homework("people_games",
                                                                                          1)) if video != "" else await callback.message.answer(
            text, reply_markup=keyboards.themes_homework("people_games", 1))
    if theme == 2:
        text = texts.video_materials_phrases[1][2]
        video = texts.video_file_ids[1][2]
        return await callback.message.answer_video(video=video, caption=text,
                                                   reply_markup=keyboards.themes_homework("people_games",
                                                                                          2)) if video != "" else await callback.message.answer(
            text, reply_markup=keyboards.themes_homework("people_games", 2))
    if theme == 3:
        text = texts.video_materials_phrases[1][3]
        video = texts.video_file_ids[1][3]
        return await callback.message.answer_video(video=video, caption=text,
                                                   reply_markup=keyboards.themes_homework("people_games",
                                                                                          3)) if video != "" else await callback.message.answer(
            text, reply_markup=keyboards.themes_homework("people_games", 3))
    if theme == 4:
        text = texts.video_materials_phrases[1][4]
        video = texts.video_file_ids[1][4]
        return await callback.message.answer_video(video=video, caption=text,
                                                   reply_markup=keyboards.themes_homework("people_games",
                                                                                          4)) if video != "" else await callback.message.answer(
            text, reply_markup=keyboards.themes_homework("people_games", 4))


@router.callback_query(F.data.startswith("contact_with_yourself_theme"))
async def people_games_theme(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.delete()
    except:
        ...
    theme = int(callback.data.split("_")[-1])
    if await utils.free_trial(callback.from_user.id):
        return await callback.message.answer(
            text=texts.no_left_time,
            reply_markup=keyboards.to_subscription_keyboard
        )
    if theme == 1:
        text = texts.video_materials_phrases[2][1]
        video = texts.video_file_ids[2][1]
        return await callback.message.answer_video(video=video, caption=text,
                                                   reply_markup=keyboards.themes_homework("contact_with_yourself",
                                                                                          1)) if video != "" else await callback.message.answer(
            text, reply_markup=keyboards.themes_homework("contact_with_yourself", 1))
    if theme == 2:
        text = texts.video_materials_phrases[2][2]
        video = texts.video_file_ids[2][2]
        return await callback.message.answer_video(video=video, caption=text,
                                                   reply_markup=keyboards.themes_homework("contact_with_yourself",
                                                                                          2)) if video != "" else await callback.message.answer(
            text, reply_markup=keyboards.themes_homework("contact_with_yourself", 2))
    if theme == 3:
        text = texts.video_materials_phrases[2][3]
        video = texts.video_file_ids[2][3]
        return await callback.message.answer_video(video=video, caption=text,
                                                   reply_markup=keyboards.themes_homework("contact_with_yourself",
                                                                                          3)) if video != "" else await callback.message.answer(
            text, reply_markup=keyboards.themes_homework("contact_with_yourself", 3))
    else:
        text = texts.video_materials_phrases[2][4]
        video = texts.video_file_ids[2][4]
        return await callback.message.answer_video(video=video, caption=text,
                                                   reply_markup=keyboards.themes_homework("contact_with_yourself",
                                                                                          4)) if video != "" else await callback.message.answer(
            text, reply_markup=keyboards.themes_homework("contact_with_yourself", 4))


@router.callback_query(F.data.startswith("birth_programs_theme"))
async def people_games_theme(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.delete()
    except:
        ...
    text = texts.video_materials_phrases[3][1]
    video = texts.video_file_ids[3][1]
    if await utils.free_trial(callback.from_user.id):
        return await callback.message.answer(
            text=texts.no_left_time,
            reply_markup=keyboards.to_subscription_keyboard
        )

    return await callback.message.answer_video(video=video, caption=text,
                                               reply_markup=keyboards.themes_homework("birth_programs",
                                                                                      1)) if video != "" else await callback.message.answer(
        text, reply_markup=keyboards.themes_homework("birth_programs", 1))


@router.callback_query(F.data.startswith("life_on_theme"))
async def people_games_theme(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.delete()
    except:
        ...
    if await utils.free_trial(callback.from_user.id):
        return await callback.message.answer(
            text=texts.no_left_time,
            reply_markup=keyboards.to_subscription_keyboard
        )
    text = texts.video_materials_phrases[4][1]
    video = texts.video_file_ids[4][1]
    return await callback.message.answer_video(video=video, caption=text,
                                               reply_markup=keyboards.themes_homework("life_on",
                                                                                      1)) if video != "" else await callback.message.answer(
        text, reply_markup=keyboards.themes_homework("life_on", 1))


@router.callback_query(F.data.startswith("presentation_"))
async def send_presentation(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception as e:
        ...
    if await utils.free_trial(callback.from_user.id):
        return await callback.message.answer(
            text=texts.no_left_time,
            reply_markup=keyboards.to_subscription_keyboard
        )
    theme = int(callback.data.split("_")[-2])
    num = int(callback.data.split('_')[-1])
    try:
        presentation_id = presentations_file_ids[theme][num]
        keyboard = keyboards.return_themes(theme)
        await callback.message.answer_document(document=presentation_id, caption="Вот презентация:", reply_markup=keyboard)
    except Exception as e:
        print("SOMETHING WENT WRONG", e)


@router.callback_query(F.data.startswith("homework_"))
async def send_homework(callback: CallbackQuery):
    await callback.answer()
    theme = int(callback.data.split("_")[-2])
    num = int(callback.data.split('_')[-1])
    try:
        await callback.message.delete()
    except:
        ...
    try:
        homework = texts.homework_text[theme][num]
        keyboard = keyboards.return_themes(theme)

        await callback.message.answer(text=homework, reply_markup=keyboard, parse_mode="HTML")
    except Exception as e:
        print("SOMETHING WENT WRONG", e)


@router.callback_query(F.data == "practices_and_techniques")
async def practices_and_techniques_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    if await utils.free_trial(callback.from_user.id):
        return await callback.message.answer(
            text=texts.no_left_time,
            reply_markup=keyboards.to_subscription_keyboard
        )
    try:
        await callback.message.edit_text(text=texts.practices_and_techniques_text,
                                         reply_markup=keyboards.practice_keyboard())
    except:
        await callback.message.answer(text=texts.practices_and_techniques_text,
                                      reply_markup=keyboards.practice_keyboard())


class Impressions(StatesGroup):
    data = State()
    get_answer = State()


@router.callback_query(F.data.startswith("practices_and_techniques_"))
async def practices_and_techniques_data_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    i, j, k = map(int, callback.data.split("_")[-3:])
    text = texts.practices_and_techniques_phrases[i][j]
    if k != 0:
        # делимся впечатлениями
        return await left_review(callback, state)
    if i == 5 and j == 1:
        audio = media.practice_pdf_ids[i][j]
        keyboard = keyboards.practices_and_techniques_keyboard_data[i][j]()
        return await callback.message.answer_audio(audio=audio, caption=text, reply_markup=keyboard)
    if j != 0:
        document = media.practice_pdf_ids[i][j]
        keyboard = keyboards.practices_and_techniques_keyboard_data[i][j]()
        return await callback.message.answer_document(document=document, caption=text, reply_markup=keyboard)

    keyboard = keyboards.practices_and_techniques_keyboard_data[i][j]()
    try:
        await callback.message.edit_text(text=text, reply_markup=keyboard)
    except:
        await callback.message.answer(text=text, reply_markup=keyboard)


@router.callback_query(F.data == "therapy")
async def therapy_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_reply_markup()
    try:
        await callback.message.edit_text(
            text=texts.therapy_text,
            reply_markup=keyboards.therapy_keyboard()
        )
    except Exception as e:
        print("EDIT_REPLY_MARKUP in therapy", e)
        await callback.message.answer(
            text=texts.therapy_text,
            reply_markup=keyboards.therapy_keyboard()
        )


@router.callback_query(F.data == "left_review")
async def left_review(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    try:
        await callback.message.edit_text(text="Оставить отзыв вы можете вот тут: @Mikekosarev",
                                         reply_markup=keyboards.to_main_menu())
    except:
        await callback.message.answer(text="Оставить отзыв вы можете вот тут: @Mikekosarev",
                                      reply_markup=keyboards.to_main_menu())


@router.callback_query(F.data == "therapy2")
async def dummy2_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    try:
        await callback.message.edit_text(text=texts.start_text, reply_markup=keyboards.to_main_menu())
    except:
        await callback.message.answer(text=texts.start_text, reply_markup=keyboards.to_main_menu())


@router.callback_query(F.data == "personal_account")
async def personal_account_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_reply_markup()
    user_id = callback.from_user.id
    status = await crud_users.get_subscription_type(user_id)
    days = await crud_users.get_user_days(user_id)
    print(status, days, type(days))
    try:
        await callback.message.edit_text(
            text=texts.personal_account_text(status, days),
            reply_markup=keyboards.personal_account_keyboard()
        )
    except Exception as e:
        await callback.message.answer(
            text=texts.personal_account_text(status, days),
            reply_markup=keyboards.personal_account_keyboard()
        )


@router.callback_query(F.data == "subscription")
async def subscription_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()
    await state.clear()
    try:
        await callback.message.answer(
            text=texts.subscription_text,
            reply_markup=keyboards.subscriptions_choose()
        )
    except:
        await callback.message.answer(
            text=texts.subscription_text,
            reply_markup=keyboards.subscriptions_choose()
        )


@router.callback_query(F.data == "first_subscription")
async def first_subscription(callback: CallbackQuery):
    await callback.answer()
    await bot.send_invoice(chat_id=callback.message.chat.id,
                           title="Доступ к боту на 30 дней",
                           description="Активация подписки на бота на 1 месяц",
                           provider_token=config.provider_token,
                           currency="rub",
                           prices=[{"label": "Доступ к боту", "amount": 990 * 100}],
                           start_parameter="start",
                           payload="first_subscription")


@router.callback_query(F.data == "second_subscription")
async def second_subscription(callback: CallbackQuery):
    await callback.answer()
    await bot.send_invoice(chat_id=callback.message.chat.id,
                           title="Доступ к боту на 30 дней + Твой Ментор",
                           description="Активация второй подписки на бота на 1 месяц",
                           provider_token=config.provider_token,
                           currency="rub",
                           prices=[{"label": "Доступ к боту+", "amount": 1590 * 100}],
                           start_parameter="start",
                           payload="second_subscription")


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    print(message.from_user.id)
    user_id = message.from_user.id
    current_type = await crud_users.get_subscription_type(user_id)
    left_days = await crud_users.get_user_days(user_id) if current_type != 0 else 0
    if message.successful_payment.invoice_payload == "first_subscription":
        sub_bought_type = 1
        await message.answer(
            text="""Супер, добро пожаловать в Your Dao клуб, по всем вопросам ты всегда можешь написать мне в личные сообщения @mikekosarev""",
            reply_markup=keyboards.to_main_menu(), parse_mode="HTML"
        )
        if int(current_type) != sub_bought_type:
            await crud_users.update_user(user_id=user_id, type="subscription_type", value=sub_bought_type)
            await crud_users.update_user(user_id=user_id, type="sub_days", value=30)
        else:
            await crud_users.update_user(user_id=user_id, type="sub_days", value=(left_days + 30))
    elif message.successful_payment.invoice_payload == "second_subscripion":
        sub_bought_type = 2
        await message.answer(
            text="""Супер, добро пожаловать в Your Dao клуб, по всем вопросам ты всегда можешь написать мне в личные сообщения @mikekosarev""",
            reply_markup=keyboards.to_main_menu(), parse_mode="HTML"
        )
        if int(current_type) != sub_bought_type:
            await crud_users.update_user(user_id=user_id, type="subscription_type", value=sub_bought_type)
            await crud_users.update_user(user_id=user_id, type="sub_days", value=30)
        else:
            await crud_users.update_user(user_id=user_id, type="sub_days", value=(left_days + 30))


@router.callback_query(F.data == "privacy_policy")
async def privacy_policy(callback: CallbackQuery):
    await callback.answer()
    doc = texts.politics_id
    cap = texts.politics_and_offers_text
    kb = keyboards.to_main_menu()
    await callback.message.answer_document(document=doc, caption=cap, reply_markup=kb)


@router.callback_query(F.data == "social_networks")
async def social_networks(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.edit_text(text=texts.social_media_text, reply_markup=keyboards.to_main_menu())
    except:
        await callback.message.answer(text=texts.social_media_text, reply_markup=keyboards.to_main_menu())


@router.callback_query(F.data == "want_bot_like_this")
async def want_bot_like_this(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.edit_text(text=texts.want_such_bot, reply_markup=keyboards.to_main_menu())
    except:
        await callback.message.answer(text=texts.want_such_bot, reply_markup=keyboards.to_main_menu())


@router.message(Command("check_pravka"))
async def check_pravka_message(message: Message):
    user_id = int(message.from_user.id)
    updates = await bot.get_updates()
    chat_messages = [update.message for update in updates if update.message and update.message.chat.id == user_id]
    print(chat_messages)
