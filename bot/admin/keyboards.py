from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

user_menu_buttons = [
    [
        InlineKeyboardButton(text="Главное меню", callback_data="start")
    ]
]
user_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=user_menu_buttons)

admin_menu_buttons = [
    [
        InlineKeyboardButton(text="Добавить пользователя", callback_data="add_user")
    ],
    [
        InlineKeyboardButton(text="Забанить пользователя", callback_data="ban_user")
    ],
    [
        InlineKeyboardButton(text="Добавить админа", callback_data="add_admin")
    ],
    [
        InlineKeyboardButton(text="Удалить", callback_data="delete_admin")
    ],
    [
        InlineKeyboardButton(text="Рассылка", callback_data="send_newsletter")
    ],
    [
        InlineKeyboardButton(text="Статистика", callback_data="statistics")
    ]
]
admin_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=admin_menu_buttons)
