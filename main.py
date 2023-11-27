import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from config import BOT_TOKEN, menu
from handlers.bestseal_handler import best_router
from handlers.history_handler import history_router
from handlers.low_high_handler import lh_router
from handlers.valute_handler import valute_router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(lh_router)
dp.include_router(best_router)
dp.include_router(history_router)
dp.include_router(valute_router)


@dp.message(CommandStart())
async def handler_start(message: types.Message):
    await message.answer(
        text=f"""Hi {message.chat.full_name} 🙂!
Я телеграм бот для поиска отелей. Я помогу найти вам 
гостиницу в зависимости от ваших потребностей. Чтобы 
узнать что я умею введите /help"""
    )


@dp.message(F.text == "/help")
async def handle_help(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Меню", reply_markup=menu)


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
