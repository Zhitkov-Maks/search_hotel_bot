from typing import List

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from database import Request, Hotel, Image
from database.settings import get_async_session


async def write_data_in_db(
        data: list,
        user_chat_id: int,
        command: str,
        count_day: int,
) -> None:
    """Функция для записи полученных данных в базу."""
    session: AsyncSession = await get_async_session()

    request_data: dict = {
        "user_chat_id": user_chat_id,
        "command": command,
    }
    request: Request = Request(**request_data)
    session.add(request)

    for htl in data:
        hotel_data: dict = {
            "address": htl["address"],
            "hotel_name": htl["name"],
            "price": float(htl["price"][1:]),
            "total_price": count_day * int(htl["price"][1:]),
            "distance": float(htl["distance"]),
        }
        hotel: Hotel = Hotel(**hotel_data)
        request.hotels.append(hotel)

        if htl["image"]:
            for img in htl["image"]:
                img_data: dict = {"image_url": img[1], "caption": img[2]}
                image: Image = Image(**img_data)
                hotel.images.append(image)

            session.add_all(hotel.images)
    session.add_all(request.hotels)
    await session.commit()


async def clean_history_data(user_chat_id: int):
    """Очистка истории запросов."""
    session = await get_async_session()
    stmt = select(Request).where(Request.user_chat_id == user_chat_id)
    requests = await session.scalars(stmt)

    for request in requests.unique().all():
        await session.delete(request)
    await session.commit()


async def data_processing(count: int, user_chat_id: int) -> List[dict]:
    """Получение данных истории запросов, отсортированных по дате.
    Возвращаем в виде списка со словарями."""
    session: AsyncSession = await get_async_session()
    total_list: list = []
    stmt = (
        select(Request)
        .where(Request.user_chat_id == user_chat_id)
        .limit(count)
        .order_by(desc(Request.time_created))
    )
    data = await session.scalars(stmt)

    for request in data.unique().all():
        for hotel in request.hotels:
            hotel_data: dict = dict()
            hotel_data["name"] = hotel.hotel_name
            hotel_data["price"] = hotel.price
            hotel_data["total_price"] = hotel.total_price
            hotel_data["address"] = hotel.address
            hotel_data["distance"] = (hotel.distance,)
            hotel_data["image"] = [(img.image_url, img.caption) for img in hotel.images]
            total_list.append(hotel_data)
    await session.close()
    return total_list
