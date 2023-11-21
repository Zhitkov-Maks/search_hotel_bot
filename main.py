import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command

from handlers.bestseal_handler import best_router
from handlers.low_high_handler import lh_router

BOT_TOKEN = "2129959600:AAHaQj719Z-rkkLf9AVNEH6OIy2pEfNnZIk"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(lh_router)
dp.include_router(best_router)


@dp.message(CommandStart())
async def handler_start(message: types.Message):
    await message.answer(
        text=f"Hi {message.chat.full_name} 🙂!\n"
             f"Я телеграмм бот для поиска отелей. Чтобы узнать что я умею "
             f"введите /help"
    )


@dp.message(Command("help", prefix="!/"))
async def handle_help(message: types.Message):
    await message.answer(
        text="Список доступных команд: "
             "\n/lowprice - Вывод самых дешёвых отелей."
             "\n/highprice - Вывод самых дорогих отелей."
             "\n/bestdeal - Вывод отелей, наиболее подходящих по цене и "
             "расположению от центра. "
             "\n/history - Вывод истории поиска отелей."
             "\n/money - В какой валюте будем искать отели?"
    )


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
