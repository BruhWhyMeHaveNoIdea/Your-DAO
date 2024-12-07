from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import bot.gpt.texts as texts
import bot.gpt.keyboards as keyboards
from bot.bot import bot

from bot.gpt.gpt_request import ask_gpt, speech_to_text

import os

router = Router()


async def convert_to_string(file_id):
    file = await bot.get_file(file_id)
    file_path = file.file_path
    destination = "bot/gpt/voices/" + file_path.split("/")[-1]
    await bot.download_file(file_path, destination)
    answer = await speech_to_text(destination)
    os.remove(destination)
    return answer




@router.callback_query(F.data == "dialogue_with_mentor")
async def dialog_with_mentor_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    try:
        await callback.message.edit_text(
            text=texts.dialogue_with_mentor_text,
            reply_markup=keyboards.dialogue_with_mentor_keyboard
        )
    except Exception as e:
        await callback.message.edit_reply_markup()
        await callback.message.answer(
            text=texts.dialogue_with_mentor_text,
            reply_markup=keyboards.dialogue_with_mentor_keyboard
        )


class GPTDialog(StatesGroup):
    history = State()  # dict of questions to gpt
    last_do = State()


@router.callback_query(F.data == "start_gpt_dialog")
async def start_gpt_dialog(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup()
    try:
        await callback.message.edit_text(
            text=texts.start_gpt_dialog_text,
            reply_markup=keyboards.gpt_menu
        )
    except Exception as e:
        print(e)
        await callback.message.answer(
            text=texts.start_gpt_dialog_text,
            reply_markup=keyboards.gpt_menu
        )
        await callback.message.edit_reply_markup()

    await state.set_state(GPTDialog.history)


@router.message(GPTDialog.history)
async def start_gpt_message(message: Message, state: FSMContext):
    try:
        await message.edit_reply_markup()
    except Exception as e:
        print(e)
        try:
            gpt_mes = (await state.get_data())["last"]
            if gpt_mes is None:
                print("pass...")
            else:
                await gpt_mes.edit_reply_markup()
                print("works....")
        except Exception as e:
            print(e)
            print("rofl...")
    print("PASSED 1")
    if not (message.text or message.voice):
        return await message.answer(
            text=texts.bad_gpt_message_type,
            reply_markup=keyboards.bad_gpt_menu
        )
    data = (await state.get_data()).get("history")
    print(f"PASSED 2, data {data}")
    if message.text:
        question = message.text
    else:
        file_id = message.voice.file_id
        question = await convert_to_string(file_id)
        if question is None:
            return await message.answer(
                text=texts.audio_not_recognized,
                reply_markup=keyboards.bad_gpt_menu
            )
        print(question)
    if data is None:
        data = [["user", question]]
    else:
        data.append(["user", question])

    bot_message = await message.answer(
        text=texts.gpt_is_thinking
    )
    print("PASSED 3")
    # gpt response
    answer = await ask_gpt(data)
    # answer to user
    gpt_answer_message = await bot_message.edit_text(
        text=answer,
        reply_markup=keyboards.gpt_keyboard,
        parse_mode="Markdown"
    )
    data.append(["assistant", answer])
    await state.update_data({"history": data})

    await state.update_data({"last": gpt_answer_message})


@router.callback_query(F.data == "clear_gpt_history")
async def clear_gpt_history_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    try:
        await callback.message.edit_reply_markup()
    except Exception as e:
        ...

    await state.update_data({"history": None})
    mes_ = await callback.message.answer(
        text=texts.gpt_dialog_clear,
        reply_markup=keyboards.gpt_menu
    )
    await state.update_data({"last": mes_})
