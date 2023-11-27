from aiogram import F
from aiogram import Router
from aiogram.types import CallbackQuery

from config import menu
from currency.currency import get_valute

valute_router = Router()


@valute_router.callback_query(F.data == "get_valute")
async def begin_work(callback: CallbackQuery):
    """Обработчик для команд get_valute"""
    get_val: tuple = await get_valute()
    await callback.message.answer(
        f"Доллар -> ${get_val[0]}\n"
        f"Евро -> €{get_val[1]}\n"
        f"Белорусский рубль -> {get_val[2]} BYN\n"
        f"Китайский юань -> ¥{get_val[3]}",
        reply_markup=menu,
    )
