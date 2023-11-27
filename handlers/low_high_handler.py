from aiogram import Router
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
    CallbackQuery,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from pydantic import ValidationError

from botrequest.serch_city import get_city_request
from config import menu
from crud.crud import write_data_in_db
from state_hotel import HotelInfoState, BestDealState
from utill.data_collection import distributor_low_high
from utill.validate_data import validate_date, check_dt_1_less_date_2

lh_router = Router()


@lh_router.callback_query(
    (F.data == "/bestdeal") | (F.data == "/highprice") | (F.data == "/lowprice")
)
async def begin_work(callback: CallbackQuery, state: FSMContext):
    """Обработчик для команд highprice, lowprice"""
    await state.update_data(command=callback.data)
    await state.set_state(HotelInfoState.city)
    await callback.message.answer(
        "Введите название города который вы хотите посетить: ",
        reply_markup=ReplyKeyboardRemove(),
    )


@lh_router.message(HotelInfoState.city)
async def enter_date_in(message: types.Message, state: FSMContext):
    """Сохранение и поиск города, если найден, то сохраняем id города."""
    await message.answer("Ждите идет поиск города....")
    search_city = await get_city_request(message.text)
    if search_city:
        await state.update_data(city=search_city[1])
        await state.set_state(HotelInfoState.date_in)
        command = await state.get_data()

        if command["command"] == "/bestdeal":
            await state.set_state(BestDealState.price_min)
            await message.answer(
                f"Город {search_city[0]} 👌 найден.\n"
                f"Укажите минимальную цену в USD. Я приму только целое число.",
                reply_markup=ReplyKeyboardRemove(),
            )
        else:
            await message.answer(
                f"Город {search_city[0]} 👌 найден.\n"
                f"Введите дату заезда в формате <дд-мм-гггг>. Будьте внимательны "
                f"не торопитесь! Дата должна быть больше текущей даты.(я проверю 😎)",
                reply_markup=ReplyKeyboardRemove(),
            )
    else:
        await state.set_state(HotelInfoState.city)
        await message.answer(
            "По вашему запросу ничего не найдено ☹️☹. Если хотите отменить поиск введите /help."
            "Если хотите продолжить то введите название города: "
        )


@lh_router.message(HotelInfoState.date_in)
async def enter_date_out(message: types.Message, state: FSMContext):
    check_date = await validate_date(message.text)

    if not check_date:
        await state.set_state(HotelInfoState.date_in)
        await message.reply(
            "ОЙ. Ошибочка. Попробуйте ещё раз. \n"
            "Введите дату заезда в формате <дд-мм-гггг>. "
            "Будьте внимательны не торопитесь! "
            "Дата должна быть больше текущей даты.(я проверю 😎)"
        )
    else:
        await state.update_data(date_in=message.text)
        await state.set_state(HotelInfoState.date_out)
        await message.answer(
            "Введите предполагаемую дату выезда. В том же формате.",
            reply_markup=ReplyKeyboardRemove(),
        )


@lh_router.message(HotelInfoState.date_out)
async def enter_date_out(message: types.Message, state: FSMContext):
    check_date = await validate_date(message.text)
    date_in = await state.get_data()
    date_out = message.text
    check_dates = await check_dt_1_less_date_2(date_in["date_in"], date_out)

    if not check_date:
        await state.set_state(HotelInfoState.date_out)
        await message.reply(
            "Недопустимый ввод! \n" "Введите дату выезда в формате <дд-мм-гггг>."
        )

    elif not check_dates:
        await state.set_state(HotelInfoState.date_in)
        await message.reply(
            "Дата выезда не может быть меньше даты заезда! \n"
            "Введите дату заезда в формате <дд-мм-гггг>."
        )

    else:
        await state.update_data(date_out=message.text, count_day=check_dates)
        await state.set_state(HotelInfoState.photo_need)
        await message.answer(
            f"Загрузить фото? Это займет больше времени.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Yes"),
                        KeyboardButton(text="No"),
                    ]
                ],
                resize_keyboard=True,
            ),
        )


@lh_router.message(HotelInfoState.photo_need, F.text.casefold() == "yes")
async def enter_count_photo(message: types.Message, state: FSMContext) -> None:
    await state.set_state(HotelInfoState.count_photo)
    builder = ReplyKeyboardBuilder()
    for i in range(1, 11):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(4)
    await message.answer(
        "Выберите число:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@lh_router.message(HotelInfoState.photo_need, F.text.casefold() == "no")
@lh_router.message(HotelInfoState.count_photo)
async def final_function(message: types.Message, state: FSMContext) -> None:
    if not message.text.isdigit() and not message.text == "no":
        await state.set_state(HotelInfoState.count_photo)
        builder = ReplyKeyboardBuilder()
        for i in range(1, 11):
            builder.add(types.KeyboardButton(text=str(i)))
        builder.adjust(4)
        await message.answer(
            "Я ожидал увидеть число. Попробуйте еще раз.",
            reply_markup=builder.as_markup(resize_keyboard=True),
        )

    else:
        if message.text.isdigit():
            await state.update_data(count_photo=int(message.text))

        elif message.text == "no":
            await state.update_data(count_photo=None)

        await message.reply(
            "Ожидайте идет сбор информации....",
            reply_markup=ReplyKeyboardRemove(),
        )

        data: dict = await state.get_data()
        command: str = data.get("command")
        count_day = data.get("count_day")
        result: list = await distributor_low_high(data)
        for mess in result:
            await message.answer(
                f"Отель: {mess['name']}\n"
                f"Цена за сутки: {mess['price']}\n"
                f"Цена за период: ${count_day * int(mess['price'][1:])}\n"
                f"Адрес: {mess['address']}\n"
                f"Расстояние до центра: {mess['distance']}Км",
                reply_markup=ReplyKeyboardRemove(),
            )
            # Подгружаем картинки
            if mess["image"]:
                for img in mess["image"]:
                    try:
                        await message.answer_photo(
                            photo=img[1],
                            caption=img[2],
                        )
                    except ValidationError:
                        await message.answer("Ошибка загрузки фото")
        await message.answer("Меню", reply_markup=menu)
        await write_data_in_db(result, message.from_user.id, command, count_day)
        await state.clear()
