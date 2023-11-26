import asyncio

from aiogram import Router
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from config import menu
from crud.crud import clean_history_data, data_processing
from state_hotel import HistoryState

history_router = Router()


@history_router.callback_query(F.data == "history")
async def begin_work_history(callback: CallbackQuery, state: FSMContext):
    """Обработчик для команд highprice, lowprice"""
    await state.set_state(HistoryState.start)
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="Показать историю",
            callback_data="show_history",
        )
    )
    builder.add(
        types.InlineKeyboardButton(
            text="Очистить историю", callback_data="clean_history"
        )
    )
    await callback.message.answer(
        "Выберите что вы хотите сделать?", reply_markup=builder.as_markup()
    )


@history_router.callback_query(F.data == "show_history")
async def show_history_func(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(HistoryState.count)
    builder = ReplyKeyboardBuilder()
    for i in range(1, 17):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(4)
    await callback.message.answer(
        "Выберите число:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@history_router.callback_query(F.data == "clean_history")
async def show_history_func(callback: types.CallbackQuery):
    await callback.message.answer(
        "Ожидайте! Идет зачистка....",
    )
    await clean_history_data(callback.from_user.id)
    await callback.message.answer(
        "История стёрта.",
    )


@history_router.message(HistoryState.count)
async def show_history_query(message: types.Message, state: FSMContext):
    await state.update_data(count=message.text)
    count = await state.get_data()
    await message.reply("Ok. Ожидайте! Идёт сбор информации....")
    result: list = await data_processing(int(count.get("count")), message.from_user.id)
    if result:
        for mess in result:
            await asyncio.sleep(3)
            await message.answer(
                f"Отель: {mess['name']}\n"
                f"Цена за сутки: ${mess['price']}\n"
                f"Цена за все время: ${mess['total_price']}\n"
                f"Адрес: {mess['address']}\n"
                f"Расстояние до центра: {mess['distance'][0]}Км",
                reply_markup=ReplyKeyboardRemove(),
            )
            # Подгружаем картинки
            if mess["image"]:
                await asyncio.sleep(0.5)
                for img in mess["image"]:
                    await message.answer_photo(
                        photo=img[0],
                        caption=img[1],
                    )
        await message.answer("Меню", reply_markup=menu)
    else:
        await message.answer("Ваша история пуста.")
    await state.clear()
