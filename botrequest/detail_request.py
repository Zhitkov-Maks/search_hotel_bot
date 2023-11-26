import asyncio
import json
from typing import Any

import jmespath

from botrequest.api_request import api_request


async def parse_request_with_photo(response: Any, photo_amt: int):
    details: list = []
    parsed_name = jmespath.search(
        "data.propertyInfo.summary.name", response
    )
    for i_photo in range(photo_amt):
        parsed_photo = jmespath.search(
            f"data.propertyInfo.propertyGallery.images[{i_photo}].image.url",
            response,
        )
        parsed_desc = jmespath.search(
            f"data.propertyInfo.propertyGallery.images[{i_photo}].image.description",
            response,
        )
        details.extend([(parsed_name, parsed_photo, parsed_desc)])

    return details


async def request_detail(payload: dict, photo_amt: int) -> list | None | bool:
    try:
        response: Any = await api_request("properties/v2/detail", payload, "POST")

        if response:
            response = json.loads(response)
            check_errors = jmespath.search("errors", response)

            if check_errors is None:
                if photo_amt is not None:
                    return await parse_request_with_photo(response, photo_amt)

                else:
                    return None

            raise PermissionError
        raise PermissionError

    except PermissionError:
        return False


async def post_detail_request(hotel: str, photo_amt: int = None) -> Any:
    """
    Функция, обрабатывающая запросы фотографий отеля.
    """
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "propertyId": hotel,
    }
    return await request_detail(payload, photo_amt)


if __name__ == "__main__":
    resp = asyncio.run(
        post_detail_request(
            hotel="74633678",
            photo_amt=None
        )
    )
    print(resp)
