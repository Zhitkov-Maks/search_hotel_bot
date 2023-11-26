import asyncio
import json
from typing import Any

import jmespath

from botrequest.api_request import api_request


async def parse_price(parsed_price: list) -> list:
    """Очищаем цену от лишних символов."""
    return [
        i_price.replace(",", "") if "," in i_price else i_price
        for i_price in parsed_price
    ]


async def generate_result(
        parsed_hotel_id: list,
        parsed_name: list,
        parsed_price_rep: list,
        parsed_distance_ftd: list,
) -> dict:
    """Функция для генерации ответа в виде словаря."""
    result = dict()
    list(
        map(
            lambda hotel_id, name, price, dist: result.update(
                {hotel_id: [name, price, dist]}
            ),
            parsed_hotel_id,
            parsed_name,
            parsed_price_rep,
            parsed_distance_ftd,
        )
    )
    if result:
        return result

    raise PermissionError


async def sorted_distance(
        parsed_distance: list,
        distance: int,
        parsed_hotel_id: list,
        parsed_name: list,
        parsed_price_rep: list,
) -> dict:
    """Функция для сортировки результата по дистанции."""
    parsed_distance_ftd = list(
        filter(lambda x: x <= distance, parsed_distance)
    )

    return await generate_result(
        parsed_hotel_id,
        parsed_name,
        parsed_price_rep,
        parsed_distance_ftd
    )


async def parse_data(response: Any, distance: int, sort: str):
    """Функция для получения необходимых данных из запроса."""
    parsed_name: list = jmespath.search(
        "data.propertySearch.properties[].name", response
    )
    parsed_hotel_id: list = jmespath.search(
        "data.propertySearch.properties[].id", response
    )
    parsed_price: list = jmespath.search(
        "data.propertySearch.properties[].price.lead.formatted", response
    )
    parsed_distance: list = jmespath.search(
        "data.propertySearch.properties[]."
        "destinationInfo.distanceFromDestination.value",
        response,
    )
    parsed_price_rep = await parse_price(parsed_price)

    length_match = jmespath.search(
        "data.propertySearch.properties", response
    )

    if sort == "DISTANCE":
        return await sorted_distance(
            parsed_distance,
            distance,
            parsed_hotel_id,
            parsed_name,
            parsed_price_rep
        )

    else:
        if len(length_match) > 0:
            return await generate_result(
                parsed_hotel_id,
                parsed_name,
                parsed_price_rep,
                parsed_distance
            )

        raise PermissionError


async def request_hotels(payload: dict, distance: int, sort: str) -> dict | bool:
    try:
        response = await api_request("properties/v2/list", payload, "POST")
        if response:
            response = json.loads(response)
            check_errors = jmespath.search("errors", response)

            if check_errors is None:
                return await parse_data(response, distance, sort)
            raise PermissionError
        raise PermissionError

    except PermissionError:
        return False


async def post_hotels_request(
        city_id: str,
        sort: str,
        date: tuple,
        price_min: int = 10,
        price_max: int = 100_000,
        hotels_amt: int = 1,
        distance: int = 0,
) -> Any:
    """Функция для генерации payload для запроса."""

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": city_id},
        "checkInDate": {
            "day": int(date[0][:2]),
            "month": int(date[0][3:5]),
            "year": int(date[0][6:]),
        },
        "checkOutDate": {
            "day": int(date[1][:2]),
            "month": int(date[1][3:5]),
            "year": int(date[1][6:]),
        },
        "rooms": [{"adults": 2, "children": [{"age": 5}, {"age": 7}]}],
        "resultsStartingIndex": 0,
        "resultsSize": hotels_amt,
        "sort": sort,
        "filters": {"price": {"max": price_max, "min": price_min}},
    }
    return await request_hotels(payload, distance, sort)


if __name__ == "__main__":
    resp = asyncio.run(
        post_hotels_request(
            city_id="2114",
            sort="PRICE_LOW_TO_HIGH",
            date=("30-12-2023", "01-05-2024"),
            price_min=30,
            price_max=500,
            distance=10,
            hotels_amt=5,
        )
    )
    print(resp)
