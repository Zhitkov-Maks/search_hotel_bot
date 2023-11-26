import asyncio

from botrequest.address_request import post_address_request
from botrequest.detail_request import post_detail_request
from botrequest.hotels_request import post_hotels_request
from database import Request
from database.settings import get_async_session


async def get_sort(command: str) -> str:
    sort = "PRICE_LOW_TO_HIGH"

    if command == "/highprice":
        sort = "PROPERTY_CLASS"

    elif command == "/bestdeal":
        sort = "DISTANCE"
    return sort


async def constructor_info(
        hotel_key: str, hotel_values: list, photo_atm: int, total_list: list
) -> dict:
    """Сбор информации по каждому отелю."""
    hotel_data = dict()
    hotel_data["name"], hotel_data["price"], hotel_data["distance"] = (
        hotel_values[0],
        hotel_values[1],
        hotel_values[2],
    )
    hotel_data["address"] = await post_address_request(hotel_key)
    hotel_data["image"] = await post_detail_request(
        hotel=hotel_key, photo_amt=photo_atm
    )
    total_list.append(hotel_data)
    return hotel_data


async def request_low_high(data: dict, sort: str):
    return await post_hotels_request(
        city_id=data.get("city"),
        sort=sort,
        date=(data.get("date_in"), data.get("date_out")),
    )


async def request_bestdeal(data, sort):
    return await post_hotels_request(
        city_id=data.get("city"),
        sort=sort,
        date=(data.get("date_in"), data.get("date_out")),
        price_min=data.get("price_min"),
        price_max=data.get("price_max"),
        distance=data.get("distance"),
    )


async def distributor_low_high(data: dict):
    """Получаем список отелей, и отдаем на сбор информации по каждому отелю."""
    total_list: list = []
    command = data.get("command")
    sort = await get_sort(command)

    if command == "/bestdeal":
        hotels = await request_bestdeal(data, sort)
    else:
        hotels = await request_low_high(data, sort)

    tasks = [
        constructor_info(hotel_key, hotel_values, data.get("count_photo"), total_list)
        for hotel_key, hotel_values in hotels.items()
    ]

    await asyncio.gather(*tasks)
    return total_list


async def main():
    session = await get_async_session()
    request_data = {
        "user_chat_id": 416484,
        "command": "/bestdeal",
    }
    request = Request(**request_data)
    session.add(request)
    await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
