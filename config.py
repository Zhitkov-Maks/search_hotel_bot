from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from decouple import config

BOT_TOKEN = config("TOKEN")
RAPIDAPI_KEY = config("RAPIDAPI_KEY")
KEY = config("KEY")

text = """Список доступных команд:
/start - Приветствие.
/help - Показать меню."""

list_base_command = [
    "/bestdeal",
    "/help",
    "/start",
    "/lowprice",
    "/highprice",
    "/history",
]

menu_bot = [
    [
        InlineKeyboardButton(text="Самые лучшие отели.", callback_data="/highprice"),
        InlineKeyboardButton(text="Самые дешёвые отели", callback_data="/lowprice"),
    ],
    [
        InlineKeyboardButton(text="По вашим данным", callback_data="/bestdeal"),
        InlineKeyboardButton(text="История ваших запросов", callback_data="history"),
    ],
    [InlineKeyboardButton(text="Узнать курсы валют.", callback_data="get_valute")]
]

menu = InlineKeyboardMarkup(inline_keyboard=menu_bot)
