import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command

from config import BOT_TOKEN, text
from handlers.bestseal_handler import best_router
from handlers.history_handler import history_router
from handlers.low_high_handler import lh_router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(lh_router)
dp.include_router(best_router)
dp.include_router(history_router)


@dp.message(CommandStart())
async def handler_start(message: types.Message):
    await message.answer(
        text=f"""Hi {message.chat.full_name} 🙂!
Я телеграм бот для поиска отелей. Я помогу найти вам 
гостиницу в зависимости от ваших потребностей. Чтобы 
узнать что я умею введите /help"""
    )


@dp.message(Command("help", prefix="!/"))
async def handle_help(message: types.Message):
    await message.answer(
        text=text
    )


@dp.message()
async def handler_start(message: types.Message):
    await message.answer(
        text=f"""Hi {message.chat.full_name} 😎😎😎! 
Я вас не понимаю. Попробуйте еще раз."""
    )


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
