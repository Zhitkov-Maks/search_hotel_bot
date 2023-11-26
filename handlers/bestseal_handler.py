from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from state_hotel import BestDealState, HotelInfoState
from utill.validate_data import check_data_digit, check_price_data

best_router = Router()


@best_router.message(BestDealState.price_min)
async def enter_date_out(message: types.Message, state: FSMContext):
    check_digit = await check_data_digit(message.text)
    if not check_digit:
        await state.set_state(BestDealState.price_min)
        await message.answer(
            "ОЙ ошибочка. Видимо вы ввели не число, давайте попробуем еще раз.\n"
            "Введите минимальную цену(Целое число).",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await state.update_data(price_min=int(message.text))
        await state.set_state(BestDealState.price_max)
        await message.answer(
            "Введите максимальную цену(Целое число).",
            reply_markup=ReplyKeyboardRemove(),
        )


@best_router.message(BestDealState.price_max)
async def enter_date_out(message: types.Message, state: FSMContext):
    check_digit = await check_data_digit(message.text)
    check_price = False
    if check_digit:
        data = await state.get_data()
        price_min = data["price_min"]
        check_price = await check_price_data(price_min, int(message.text))

    if not check_digit:
        await state.set_state(BestDealState.price_max)
        await message.answer(
            "ОЙ ошибочка. Видимо вы ввели не число, давайте попробуем еще раз.\n"
            "Введите максимальную цену(Целое число).",
            reply_markup=ReplyKeyboardRemove(),
        )

    elif not check_price:
        await state.set_state(BestDealState.price_max)
        await message.answer(
            "ОЙ ошибочка. Видимо вы ввели не число, давайте попробуем еще раз.\n"
            "Введите максимальную цену(Целое число).",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
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
