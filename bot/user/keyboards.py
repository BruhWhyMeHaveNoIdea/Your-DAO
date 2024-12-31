from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import bot.user.utils as utils


def to_main_menu():
    buttons = [
        [
            InlineKeyboardButton(text="В меню", callback_data="start")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def start_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="Видеоматериалы", callback_data="video_materials")
        ],
        [
            InlineKeyboardButton(text="Практики и техники", callback_data="practices_and_techniques")
        ],
        [
            InlineKeyboardButton(text="Диалог с наставником", callback_data="dialogue_with_mentor")
        ],
        [
            InlineKeyboardButton(text="Терапия", callback_data="therapy")
        ],
        [
            InlineKeyboardButton(text="Чат", callback_data="chat")
        ],
        [
            InlineKeyboardButton(text="Личный кабинет", callback_data="personal_account")
        ],
        [
            InlineKeyboardButton(text="Оставить отзыв", callback_data="left_review")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def therapy_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="Записаться на сессию", url="https://t.me/mikekosarev")
        ],
        [
            InlineKeyboardButton(text="Узнать про проект", callback_data="therapy2")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="start")
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def video_materials_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="Модуль - Игры людей", callback_data="people_games")
        ],
        [
            InlineKeyboardButton(text="Модуль - Контакт с собой", callback_data="contact_with_yourself")
        ],
        [
            InlineKeyboardButton(text="Модуль - Родовые программы", callback_data="birth_programs")
        ],
        [
            InlineKeyboardButton(text="Модуль - Включение жизни", callback_data="life_on")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="start")
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def personal_account_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="Подписка", callback_data="subscription"),
        ],
        [
            InlineKeyboardButton(text="Публичная оферта и политика конфиденциальности", callback_data="privacy_policy")
        ],
        [
            InlineKeyboardButton(text="Социальные сети", callback_data="social_networks")
        ],
        [
            InlineKeyboardButton(text="Хочу такого же бота", callback_data="want_bot_like_this")
        ],
        [
            InlineKeyboardButton(text="В главное меню", callback_data="start")
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def subscription_keyboard(url1, url2):
    buttons = [
        [
            InlineKeyboardButton(text="Доступ к урокам - 990 рублей", url=url1)
        ],
        [
            InlineKeyboardButton(text="Доступ к урокам и диалогу - 1590 рублей", url=url2)
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="start")
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_referral_keyboard(bonuses):
    back = InlineKeyboardButton(text="Назад", callback_data="personal_account")
    if bonuses == 0:
        return InlineKeyboardMarkup(inline_keyboard=[[back]])
    one_bonus = InlineKeyboardButton(text="Потратить 1 бонус", callback_data="spend_bonuses_1")
    if bonuses == 1:
        return InlineKeyboardMarkup(inline_keyboard=[[one_bonus], [back]])
    all_bonuses = InlineKeyboardButton(text="Потратить все бонусы", callback_data=f"spend_bonuses_{bonuses}")
    return InlineKeyboardMarkup(inline_keyboard=[[one_bonus], [all_bonuses], [back]])


def people_games_theme():
    buttons = [
        [InlineKeyboardButton(text="Основы восприятия", callback_data="people_games_theme_1")],
        [InlineKeyboardButton(text="Модели поведения. Темпераменты.", callback_data="people_games_theme_2")],
        [InlineKeyboardButton(text="Архетипы", callback_data="people_games_theme_3")],
        [InlineKeyboardButton(text="Назад", callback_data="video_materials")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


to_subscription_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Приобрести подписку", callback_data="subscription")]])


def contact_with_yourself():
    buttons = [
        [InlineKeyboardButton(text="Эмоциональная свобода ", callback_data="contact_with_yourself_theme_1")],
        [InlineKeyboardButton(text="Тело и психосоматика", callback_data="contact_with_yourself_theme_2")],
        [InlineKeyboardButton(text="Психоэнергетическое состояние", callback_data="contact_with_yourself_theme_3")],
        [InlineKeyboardButton(text="Внутренняя свобода без вины и стыда",
                              callback_data="contact_with_yourself_theme_4")],
        [InlineKeyboardButton(text="Назад", callback_data="video_materials")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def birth_programs():
    buttons = [
        [InlineKeyboardButton(text="Родовые программы и карма. Научный подход",
                              callback_data="birth_programs_theme_1")],
        [InlineKeyboardButton(text="Назад", callback_data="video_materials")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def life_on():
    buttons = [
        [InlineKeyboardButton(text="Жизненные циклы и управление потоком жизни", callback_data="life_on_theme_1")],
        [InlineKeyboardButton(text="Назад", callback_data="video_materials")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def themes_homework(theme: str, num: int):
    count = utils.recieve_num(theme, 1)
    buttons = [
        [InlineKeyboardButton(text="Посмотреть презентацию", callback_data=f"presentation_{count}_{num}")],
        [InlineKeyboardButton(text="Домашнее задание", callback_data=f"homework_{count}_{num}")],
        [InlineKeyboardButton(text="Назад", callback_data=f"{theme}")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def return_themes(theme):
    name = utils.recieve_num(theme - 1, 2)
    button = [[InlineKeyboardButton(text="Назад к уроку", callback_data=f"{name}")]]
    print(button)
    return InlineKeyboardMarkup(inline_keyboard=button)


# Функция для генерации клавиатуры
def generate_keyboard(buttons_data):
    buttons = [
        [InlineKeyboardButton(text=label, callback_data=callback)]
        for label, callback in buttons_data
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def practice_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="Перепрошивка мозга", callback_data="practices_and_techniques_1_0_0")
        ],
        [
            InlineKeyboardButton(text="Любовь к себе", callback_data="practices_and_techniques_2_0_0")
        ],
        [
            InlineKeyboardButton(text="Работа с телом и энергией", callback_data="practices_and_techniques_3_0_0")
        ],
        [
            InlineKeyboardButton(text="Медитация для сна", callback_data="practices_and_techniques_4_1_0")
        ],
        [
            InlineKeyboardButton(text="Активация управления жизнью ", callback_data="practices_and_techniques_5_1_0")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="start")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


practices_and_techniques_keyboard_data = {
    1: {
        0: lambda: generate_keyboard([
            ("Практика самоанализа", "practices_and_techniques_1_1_0"),
            ("Практика депрограмминг", "practices_and_techniques_1_2_0"),
            ("Практика активации желаний", "practices_and_techniques_1_3_0"),
            ("Практика дневник побед", "practices_and_techniques_1_4_0"),
            ("Назад", "practices_and_techniques")
        ]),
        1: lambda: generate_keyboard([
            ("Поделиться впечатлениями", "practices_and_techniques_1_1_1"),
            ("Назад", "practices_and_techniques_1_0_0")
        ]),
        2: lambda: generate_keyboard([
            ("Поделиться впечатлениями", "practices_and_techniques_1_2_1"),
            ("Назад", "practices_and_techniques_1_0_0")
        ]),
        3: lambda: generate_keyboard([
            ("Поделиться впечатлениями", "practices_and_techniques_1_3_1"),
            ("Назад", "practices_and_techniques_1_0_0")
        ]),
        4: lambda: generate_keyboard([
            ("Поделиться впечатлениями", "practices_and_techniques_1_4_1"),
            ("Назад", "practices_and_techniques_1_0_0")
        ])

    },
    2: {
        0: lambda: generate_keyboard([
            ("Практика любви к себе", "practices_and_techniques_2_1_0"),
            ("Таблица благодарности", "practices_and_techniques_2_2_0"),
            ("Практика прощения и отпускания", "practices_and_techniques_2_3_0"),
            ("Назад", "practices_and_techniques")
        ]),
        1: lambda: generate_keyboard([
            ("Поделиться впечатлениями", "practices_and_techniques_2_1_1"),
            ("Назад", "practices_and_techniques_2_0_0")
        ]),
        2: lambda: generate_keyboard([
            ("Поделиться впечатлениями", "practices_and_techniques_2_2_1"),
            ("Назад", "practices_and_techniques_2_0_0")
        ]),
        3: lambda: generate_keyboard([
            ("Поделиться впечатлениями", "practices_and_techniques_2_3_1"),
            ("Назад", "practices_and_techniques_2_0_0")
        ]),
    },
    3: {
        0: lambda: generate_keyboard([
            ("Практика медитаций", "practices_and_techniques_3_1_0"),
            ("Дыхательные практики", "practices_and_techniques_3_2_0"),
            ("Техники работы с телом", "practices_and_techniques_3_3_0"),
            ("Аффирмации и работа с энергией", "practices_and_techniques_3_4_0"),
            ("Назад", "practices_and_techniques")
        ]),

        1: lambda: generate_keyboard([
            ("Поделиться впечатлениями", "practices_and_techniques_3_1_1"),
            ("Назад", "practices_and_techniques_3_0_0")
        ]),
        2: lambda: generate_keyboard([
            ("Поделиться впечатлениями", "practices_and_techniques_3_2_1"),
            ("Назад", "practices_and_techniques_3_0_0")
        ]),
        3: lambda: generate_keyboard([
            ("Поделиться впечатлениями", "practices_and_techniques_3_3_1"),
            ("Назад", "practices_and_techniques_3_0_0")
        ]),
        4: lambda: generate_keyboard([
            ("Поделиться впечатлениями", "practices_and_techniques_3_4_1"),
            ("Назад", "practices_and_techniques_3_0_0")
        ])
    },
    4: {
        1: lambda: generate_keyboard([
            ("Поделиться впечатлениями", "practices_and_techniques_4_1_1"),
            ("Назад", "practices_and_techniques")
        ])
    },
    5: {
        1: lambda: generate_keyboard([
            ("Поделиться впечатлениями", "practices_and_techniques_5_1_1"),
            ("Назад", "practices_and_techniques")
        ])
    }
}


def back_practices_and_techniques_keyboard(i, j):
    buttons = [
        [
            InlineKeyboardButton(text="Назад", callback_data=f"practices_and_techniques_{i}_{j}_0")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def subscriptions_choose():
    buttons = [[
        InlineKeyboardButton(text="990 - Доступ на 30 дней", callback_data="first_subscription")
    ],
    [
        InlineKeyboardButton(text="1590 - Доступ + Твой ментор", callback_data="second_subscription")
    ],
    [
        InlineKeyboardButton(text="В меню", callback_data="start")
    ]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
