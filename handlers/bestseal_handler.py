from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from state_hote import BestDealState, HotelInfoState

best_router = Router()


@best_router.message(BestDealState.price_min)
async def enter_date_out(message: types.Message, state: FSMContext):
    await state.update_data(price_min=int(message.text))
    await state.set_state(BestDealState.price_max)
    await message.answer(
        "Введите максимальную цену.",
        reply_markup=ReplyKeyboardRemove(),
    )


@best_router.message(BestDealState.price_max)
async def enter_date_out(message: types.Message, state: FSMContext):
    await state.update_data(price_max=int(message.text))
    await state.set_state(BestDealState.distance)
    await message.answer(
        "Введите расстояние до центра. (Целое число)",
        reply_markup=ReplyKeyboardRemove(),
    )


@best_router.message(BestDealState.distance)
async def enter_date_out(message: types.Message, state: FSMContext):
    await state.update_data(distance=int(message.text))
    await state.set_state(HotelInfoState.date_in)
    await message.answer(
        "Введите дату заезда в формате <дд-мм-гггг>",
        reply_markup=ReplyKeyboardRemove(),
    )
