import datetime

from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.types import InputMediaVideo, InputMediaDocument
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


async def send_aiogram_message(callback, text, reply_markup):
    try:
        await callback.message.edit_text(text=text, reply_markup=reply_markup)
    except:
        await callback.message.answer(text=text, reply_markup=reply_markup)


async def send_aiogram_video(callback, video, caption, reply_markup):
    try:
        await callback.message.edit_media(InputMediaVideo(media=video), caption=caption, reply_markup=reply_markup)
    except:
        await callback.message.answer_video(video, caption=caption, reply_markup=reply_markup)


async def send_aiogram_document(callback, document, caption, reply_markup):
    try:
        await callback.message.edit_media(InputMediaDocument(media=document), caption=caption,
                                          reply_markup=reply_markup)
    except:
        await callback.message.answer_document(document, caption=caption, reply_markup=reply_markup)


async def send_aiogram_audio(callback, audio, text, reply_markup):
    try:
        await callback.message.delete()
        await callback.message.answer_audio(InputMediaDocument(media=audio), caption=text,
                                            reply_markup=reply_markup)
    except:
        await callback.message.answer_audio(audio, caption=text, reply_markup=reply_markup)


@router.message(Command("get_ref"))
async def get_ref(message: Message):
    bot_name = (await bot.me()).username()
    return await message.answer(
        text=f"https://t.me/{bot_name}?start={message.from_user.id}"
    )


@router.message(Command('start'))
async def start_command(message: Message, state: FSMContext):
    await state.clear()

    user_id = (message.from_user.id)
    if (await crud_banned.read_banned(message.from_user.username)):
        print("ban")
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
            active=0,
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
    if (await crud_users.get_subscription_type(user_id)) == 0:
        return await callback.message.answer(
            text=texts.no_access_to_materials,
            reply_markup=keyboards.to_subscription_keyboard
        )
    await callback.answer()
    await callback.message.answer(text="Ссылка на чат")


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

    await send_aiogram_message(callback, texts.video_materials_text, keyboards.video_materials_keyboard())


@router.callback_query(F.data == "people_games")
async def people_games(callback: CallbackQuery):
    await callback.answer()
    await send_aiogram_message(callback, "Сообщение [1 модуль]", keyboards.people_games_theme())


@router.callback_query(F.data == "contact_with_yourself")
async def contact_with_yourself(callback: CallbackQuery):
    await callback.answer()
    await send_aiogram_message(callback, "Сообщение [2 модуль]", keyboards.contact_with_yourself())


@router.callback_query(F.data == "birth_programs")
async def birth_programs(callback: CallbackQuery):
    await callback.answer()
    await send_aiogram_message(callback, "Сообщение [3 модуль]", keyboards.birth_programs())


@router.callback_query(F.data == "life_on")
async def life_on(callback: CallbackQuery):
    await callback.answer()
    await send_aiogram_message(callback, "Сообщение [4 модуль]", keyboards.life_on())


@router.callback_query(F.data.startswith("people_games_theme"))
async def people_games_theme(callback: CallbackQuery):
    await callback.answer()
    theme = int(callback.data.split("_")[-1])
    if theme == 1:
        text = texts.video_materials_phrases[1][1]
        video = texts.video_file_ids[1][1]
        return await send_aiogram_video(callback, video, text, keyboards.themes_homework("people_games",
                                                                                         1)) if video != "" else await send_aiogram_message(
            callback, text, keyboards.themes_homework("people_games", 1))
    if theme == 2:
        text = texts.video_materials_phrases[1][2]
        video = texts.video_file_ids[1][2]
        return await send_aiogram_video(callback, video, text, keyboards.themes_homework("people_games",
                                                                                         1)) if video != "" else await send_aiogram_message(
            callback, text, keyboards.themes_homework("people_games", 1))
    else:
        text = texts.video_materials_phrases[1][3]
        video = texts.video_file_ids[1][3]
        return await send_aiogram_video(callback, video, text, keyboards.themes_homework("people_games",
                                                                                         1)) if video != "" else await send_aiogram_message(
            callback, text, keyboards.themes_homework("people_games", 1))


@router.callback_query(F.data.startswith("contact_with_yourself_theme"))
async def people_games_theme(callback: CallbackQuery):
    await callback.answer()
    theme = int(callback.data.split("_")[-1])
    if theme == 1:
        text = texts.video_materials_phrases[2][1]
        video = texts.video_file_ids[2][1]
        return await send_aiogram_video(callback, video, text, keyboards.themes_homework("contact_with_yourself",
                                                                                         1)) if video != "" else await send_aiogram_message(
            callback, text, keyboards.themes_homework("contact_with_yourself", 1))
    if theme == 2:
        text = texts.video_materials_phrases[2][2]
        video = texts.video_file_ids[2][2]
        return await send_aiogram_video(callback, video, text, keyboards.themes_homework("contact_with_yourself",
                                                                                         1)) if video != "" else await send_aiogram_message(
            callback, text, keyboards.themes_homework("contact_with_yourself", 1))
    else:
        text = texts.video_materials_phrases[2][3]
        video = texts.video_file_ids[2][3]
        return await send_aiogram_video(callback, video, text, keyboards.themes_homework("contact_with_yourself",
                                                                                         1)) if video != "" else await send_aiogram_message(
            callback, text, keyboards.themes_homework("contact_with_yourself", 1))


@router.callback_query(F.data.startswith("birth_programs_theme"))
async def people_games_theme(callback: CallbackQuery):
    await callback.answer()
    text = texts.video_materials_phrases[3][1]
    video = texts.video_file_ids[3][1]
    return await send_aiogram_video(callback, video, text, keyboards.themes_homework("birth_programs",
                                                                                     1)) if video != "" else await send_aiogram_message(
        callback, text, keyboards.themes_homework("birth_programs", 1))


@router.callback_query(F.data.startswith("life_on_theme"))
async def people_games_theme(callback: CallbackQuery):
    await callback.answer()
    text = texts.video_materials_phrases[4][1]
    video = texts.video_file_ids[4][1]
    return await send_aiogram_video(callback, video, text, keyboards.themes_homework("life_on",
                                                                                     1)) if video != "" else await send_aiogram_message(
        callback, text, keyboards.themes_homework("life_on", 1))


@router.callback_query(F.data.startswith("presentation_"))
async def send_presentation(callback: CallbackQuery):
    await callback.answer()
    theme = int(callback.data.split("_")[-2])
    num = int(callback.data.split('_')[-1])
    try:
        presentation_id = presentations_file_ids[theme][num]
        print(presentation_id)
        keyboard = keyboards.return_themes(theme)
        await send_aiogram_document(callback, presentation_id, "", keyboard)
    except Exception as e:
        print(e)
        print("SOMETHING WENT WRONG")


@router.callback_query(F.data.startswith("homework_"))
async def send_homework(callback: CallbackQuery):
    await callback.answer()
    theme = int(callback.data.split("_")[-2])
    num = int(callback.data.split('_')[-1])
    try:
        homework = texts.homework_text[theme][num]
        keyboard = keyboards.return_themes(theme)
        await send_aiogram_message(callback, homework, keyboard)
    except Exception as e:
        print(e)
        print("SOMETHING WENT WRONG")


@router.callback_query(F.data == "practices_and_techniques")
async def practices_and_techniques_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    await send_aiogram_message(callback, texts.practices_and_techniques_text, keyboards.practice_keyboard())


class Impressions(StatesGroup):
    data = State()
    get_answer = State()


@router.callback_query(F.data.startswith("practices_and_techniques_"))
async def practices_and_techniques_data_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    i, j, k = map(int, callback.data.split("_")[-3:])
    print(i, j, k)
    if k != 0:
        # делимся впечатлениями
        await send_aiogram_message(callback, "Поделитесь впечатлениями",
                                   keyboards.back_practices_and_techniques_keyboard(i, j))
        await state.set_state(Impressions.get_answer)
        await state.update_data({"data": [i, j]})
        return
    if i == 5 and j == 1:
        audio = media.practice_pdf_ids[i][j]
        text = texts.practice_text
        keyboard = keyboards.practices_and_techniques_keyboard_data[i][j]()
        return await send_aiogram_audio(callback, audio, text, keyboard)
    if j != 0:
        document = media.practice_pdf_ids[i][j]
        text = texts.practice_text
        keyboard = keyboards.practices_and_techniques_keyboard_data[i][j]()
        return await send_aiogram_document(callback, document, text, keyboard)

    text = texts.practices_and_techniques_phrases[i][j]
    keyboard = keyboards.practices_and_techniques_keyboard_data[i][j]()

    await send_aiogram_message(callback, text, keyboard)


@router.message(Impressions.get_answer)
async def get_answer_message(message: Message, state: FSMContext):
    i, j = (await state.get_data())["data"]
    await message.answer(
        text="SENT!",

    )


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


@router.callback_query(F.data == "therapy2")
async def dummy2_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.answer(text=texts.start_text, reply_markup=keyboards.to_main_menu())


@router.callback_query(F.data == "personal_account")
async def personal_account_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_reply_markup()

    try:
        await callback.message.edit_text(
            text=texts.personal_account_text,
            reply_markup=keyboards.personal_account_keyboard()
        )
    except Exception as e:
        print("EDIT_REPLY_MARKUP in therapy", e)
        await callback.message.answer(
            text=texts.personal_account_text,
            reply_markup=keyboards.personal_account_keyboard()
        )


@router.callback_query(F.data == "subscription")
async def subscription_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()
    await state.clear()
    user_id = int(callback.from_user.id)

    await callback.message.answer(
        text=texts.subscription_text,
        reply_markup=keyboards.subscriptions_choose()
    )


@router.callback_query(F.data == "first_subscription")
async def first_subscription(callback: CallbackQuery):
    await bot.send_invoice(chat_id=callback.message.chat.id,
                           title="Подписка на бота",
                           description="Активация первой подписки на бота на 1 месяц",
                           provider_token=config.provider_token,
                           currency="rub",
                           prices=[{"label": "Второй вариант подписки", "amount": 1*100}],
                           start_parameter="start",
                           payload="first_subscription")


@router.callback_query(F.data == "second_subscription")
async def second_subscription(callback: CallbackQuery):
    await bot.send_invoice(chat_id=callback.message.chat.id,
                           title="Подписка на бота",
                           description="Активация второй подписки на бота на 1 месяц",
                           provider_token=config.provider_token,
                           currency="rub",
                           prices=[{"label": "Второй вариант подписки", "amount": 1590*100}],
                           start_parameter="start",
                           payload="second_subscription")


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    print(message.from_user.id)
    user_id=message.from_user.id
    current_type = await crud_users.get_subscription_type(user_id)
    left_days = await crud_users.get_user_days(user_id) if current_type != 0 else 0
    if message.successful_payment.invoice_payload == "first_subscription":
        sub_bought_type = 1
        await message.answer(
            text="[Сообщение с благодарностью за 1 подписку]",
            reply_markup=keyboards.to_main_menu(), parse_mode="HTML"
        )
        if int(current_type) != sub_bought_type:
            await crud_users.update_user(user_id=user_id,type="subscription_type", value=sub_bought_type)
            await crud_users.update_user(user_id=user_id,type="sub_days",value=30)
        else:
            await crud_users.update_user(user_id=user_id,type="sub_days",value=(left_days+30))
    elif message.successful_payment.invoice_payload == "second_subscripion":
        sub_bought_type = 2
        await message.answer(
            text="[Сообщение с благодарностью за 2 подписку]",
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
    await callback.message.answer(text=texts.politics_and_offers_text, reply_markup=keyboards.to_main_menu())


@router.callback_query(F.data == "social_networks")
async def social_networks(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(text=texts.social_media_text, reply_markup=keyboards.to_main_menu())


@router.callback_query(F.data == "want_bot_like_this")
async def want_bot_like_this(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(text=texts.want_such_bot, reply_markup=keyboards.to_main_menu())


@router.callback_query(F.data.startswith("spend_bonuses_"))
async def start_bonuses_n_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    user_id = int(callback.from_user.id)
    bonuses = int(callback.data.split("_")[-1])


# @router.message()
# async def check_types(message: Message):
#     if message.photo:
#         file_id = message.photo[0].file_id
#         await message.answer_photo(
#             photo=file_id,
#             caption=f'PHOTO\n<code>{message.photo[0].file_id}</code>'
#         )
#     elif message.document:
#         file_id = message.document.file_id
#         await message.answer_document(
#             document=file_id,
#             caption=f'DOCUMENT\n<code>{file_id}</code>'
#         )
#     elif message.video:
#         file_id = message.video.file_id
#         await message.answer_video(
#             video=file_id,
#             caption=f'VIDEO\n<code>{file_id}</code>'
#         )
#     elif message.audio:
#         file_id = message.audio.file_id
#         await message.answer_audio(
#             audio=file_id,
#             caption=f'audio\n<code>{file_id}</code>'
#         )
#     else:
#         return
