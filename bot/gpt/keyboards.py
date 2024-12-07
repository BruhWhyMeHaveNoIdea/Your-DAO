from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

dialog_with_mentor_buttons = [
    [
        InlineKeyboardButton(text="Запустить диалог", callback_data="start_gpt_dialog")
    ],
    [
        InlineKeyboardButton(text="Назад", callback_data="start")
    ]
]

dialogue_with_mentor_keyboard = InlineKeyboardMarkup(inline_keyboard=dialog_with_mentor_buttons)

gpt_menu_buttons = [
    [
        InlineKeyboardButton(text="Выйти в главное меню", callback_data="start")
    ]
]
gpt_menu = InlineKeyboardMarkup(inline_keyboard=gpt_menu_buttons)

bad_gpt_menu_buttons = [
    [
        InlineKeyboardButton(text="Закончить чат", callback_data="dialogue_with_mentor")
    ],
    [
        InlineKeyboardButton(text="Выйти в главное меню", callback_data="start")
    ]
]
bad_gpt_menu = InlineKeyboardMarkup(inline_keyboard=bad_gpt_menu_buttons)

gpt_buttons = [
    [
        InlineKeyboardButton(text="Стереть память GPT", callback_data="clear_gpt_history")
    ],
    [
        InlineKeyboardButton(text="Закончить чат", callback_data="dialogue_with_mentor")
    ],
]

gpt_keyboard = InlineKeyboardMarkup(inline_keyboard=gpt_buttons)
