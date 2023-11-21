from aiogram import Router
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

from botrequest.serch_city import get_city_request
from data_collection import distributor_low_high
from state_hote import HotelInfoState, BestDealState
from utill.validate_data import validate_date, check_dt_1_less_date_2

lh_router = Router()


@lh_router.message(
    (F.text == "/bestdeal") | (F.text == "/highprice") | (F.text == "/lowprice")
)
async def begin_work(message: types.Message, state: FSMContext):
    """Обработчик для команд highprice, lowprice"""
    await state.update_data(command=message.text)
    await state.set_state(HotelInfoState.city)
    await message.answer(
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
                f"Город {search_city[0]} 👌 найден.\n" "Укажите минимальную цену.",
                reply_markup=ReplyKeyboardRemove(),
            )
        else:
            await message.answer(
                f"Город {search_city[0]} 👌 найден.\n"
                f"Введите дату заезда в формате <дд-мм-гггг>.",
                reply_markup=ReplyKeyboardRemove(),
            )
    else:
        await state.set_state(HotelInfoState.city)
        await message.answer(
            "По вашему запросу ничего не найдено ☹️☹. Попробуйте еще раз.\n"
            "Введите название города: "
        )


@lh_router.message(HotelInfoState.date_in)
async def enter_date_out(message: types.Message, state: FSMContext):
    check_date = await validate_date(message.text)

    if not check_date:
        await state.set_state(HotelInfoState.date_in)
        await message.reply(
            "Недопустимый ввод! \n" "Введите дату заезда в формате <дд-мм-гггг>."
        )
    else:
        await state.update_data(date_in=message.text)
        await state.set_state(HotelInfoState.date_out)
        await message.answer(
            "Предполагаемая дата выезда: ",
            reply_markup=ReplyKeyboardRemove(),
        )


@lh_router.message(HotelInfoState.date_out)
async def enter_date_out(message: types.Message, state: FSMContext):
    check_date = await validate_date(message.text)
    date_in = await state.get_data()
    check_dates = await check_dt_1_less_date_2(date_in["date_in"], message.text)
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
        await state.update_data(date_out=message.text)
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
    await message.reply(
        "Сколько фотографий вы хотели бы увидеть?",
        reply_markup=ReplyKeyboardRemove(),
    )


@lh_router.message(HotelInfoState.photo_need, F.text.casefold() == "no")
@lh_router.message(HotelInfoState.count_photo)
async def final_function(message: types.Message, state: FSMContext) -> None:
    if message.text.isdigit():
        await state.update_data(count_photo=int(message.text))
    else:
        await state.update_data(count_photo=None)
    await message.reply(
        "Ожидайте идет сбор информации....",
        reply_markup=ReplyKeyboardRemove(),
    )
    data = await state.get_data()
    result = await distributor_low_high(data)

    for mess in result:
        await message.answer(
            f"Отель: {mess['name']}\n"
            f"Цена за сутки: {mess['price']}\n"
            f"Адрес: {mess['address']}\n"
            f"Расстояние до центра: {mess['distance']}Км",
            reply_markup=ReplyKeyboardRemove(),
        )
        # Подгружаем картинки
        if mess["image"]:
            for img in mess["image"]:
                await message.answer_photo(
                    photo=img[1],
                    caption=img[2],
                )
