from aiogram.fsm.state import StatesGroup, State


class HotelInfoState(StatesGroup):
    """Класс состояний для команд: /lowprice, /highprice"""

    city = State()
    date_in = State()
    date_out = State()
    photo_need = State()
    command = State()
    count_photo = State()
    count_hotel = State()


class BestDealState(HotelInfoState):
    """Класс состояний для команды /bestdeal"""

    price_min = State()
    price_max = State()
    distance = State()
