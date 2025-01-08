from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from lexicon.lexicon import *


# функция-комбайнер, генерация кнопок главного меню
def create_keys(wight: int, *args: str, **kwargs: str):
    # инициализация биллдера для клавиатуры основного меню
    menu: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    # Инициализация кнопок
    buttons: list[KeyboardButton] = []

    if args:
        for button in args:
            buttons.append(KeyboardButton(text=button))

    if kwargs:
        for key, value in kwargs.items():
            buttons.append(KeyboardButton(text=value, resize_keyboard=True))

    menu.row(*buttons, width=wight)
    return menu.as_markup()


# функция-комбайнер, выбор базы для добавления
def create_inline_keys(wight: int, *args: str, **kwargs: str):
    # инициализация биллдера для клавиатуры создания записи
    inline_button: InlineKeyboardBuilder = InlineKeyboardBuilder()

    # Инициализация кнопок
    buttons: list[InlineKeyboardButton] = []

    if args:
        for button in args:
            buttons.append(
                InlineKeyboardButton(
                    text=INLINE_BUTTON[button] if button in INLINE_BUTTON else button,
                    callback_data=button
                )
            )

    if kwargs:
        for key, value in kwargs.items():
            buttons.append(InlineKeyboardButton(text=value, callback_data=key))

    inline_button.row(*buttons, width=wight)
    return inline_button.as_markup()


# Кнопка регистрации
# Создание инлайн-кнопки
reg_button = InlineKeyboardButton(text='Регистрация', callback_data='reg')
# Создание инлайн-клавиатуры
keyboard_reg = InlineKeyboardMarkup(inline_keyboard=[[reg_button], ])

# Клавиатура админа
# Создание инлайн-кнопок
button_spam = InlineKeyboardButton(
    text=INLINE_BUTTON_ADMIN['admin_1'],
    callback_data='admin_1'
)

button_stat = InlineKeyboardButton(
    text=INLINE_BUTTON_ADMIN['admin_2'],
    callback_data='admin_2'
)

button_blacklist = InlineKeyboardButton(
    text=INLINE_BUTTON_ADMIN['admin_3'],
    callback_data='admin_3'
)

button_whitelist = InlineKeyboardButton(
    text=INLINE_BUTTON_ADMIN['admin_4'],
    callback_data='admin_4'
)

# Создание инлайн-клавиатуры
keyboard_inline_admin = InlineKeyboardMarkup(
    inline_keyboard=[[button_spam, button_stat], [button_blacklist, button_whitelist]]
)

# Клавиатура для добавления/или не ссылки в базу
button_yes = InlineKeyboardButton(
    text=INLINE_BUTTON_STORE['add_3'],
    callback_data='add_3'
)

button_no = InlineKeyboardButton(
    text=INLINE_BUTTON_STORE['add_4'],
    callback_data='add_4'
)

keyboard_inline_add_address = InlineKeyboardMarkup(inline_keyboard=[[button_yes, button_no]])

# Кнопка "готово" для списка
# Создание инлайн-кнопки
ready_store = InlineKeyboardButton(text='Готово', callback_data='ready')
# Создание инлайн-клавиатуры
keyboard_ready_store = InlineKeyboardMarkup(inline_keyboard=[[ready_store], ])

# Клавиатура повтора для календаря
# Создание инлайн-кнопок
repeat_no = InlineKeyboardButton(text='Без повторов', callback_data='repeat_no')
repeat_month = InlineKeyboardButton(text='Ежемесячно', callback_data='repeat_month')
repeat_year = InlineKeyboardButton(text='Ежегодно', callback_data='repeat_year')
# Создание инлайн-клавиатуры
keyboard_inline_repeat_calendar = InlineKeyboardMarkup(inline_keyboard=[[repeat_no, repeat_month, repeat_year], ])

# Кнопка "готово" для календаря
# Создание инлайн-кнопки
ready_calendar = InlineKeyboardButton(text='Готово', callback_data='ready_calendar')
# Создание инлайн-клавиатуры
keyboard_ready_calendar = InlineKeyboardMarkup(inline_keyboard=[[ready_calendar], ])
