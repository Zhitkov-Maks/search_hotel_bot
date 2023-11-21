import asyncio
import json
from pprint import pprint
from typing import Any

import jmespath

from botrequest.api_request import api_request


async def post_detail_request(hotel: str, photo_amt: int = None) -> Any:
    """
    Функция, обрабатывающая запросы фотографий отеля,
    а также фотографии для inline-кнопки 'На карте'
    """
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "propertyId": hotel,
    }

    try:
        response = await api_request("properties/v2/detail", payload, "POST")

        if response:
            response = json.loads(response)
            pprint(response)
            check_errors = jmespath.search("errors", response)

            if check_errors is None:
                if photo_amt is not None:
                    details = []
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
                        # details[parsed_name].append({parsed_photo: parsed_desc})
                        details.extend([(parsed_name, parsed_photo, parsed_desc)])

                    return details

                else:
                    details = list()
                    parsed_name = jmespath.search(
                        "data.propertyInfo.summary.name", response
                    )
                    parsed_address = jmespath.search(
                        "data.propertyInfo." "summary.location." "address.addressLine",
                        response,
                    )
                    parsed_static_img = jmespath.search(
                        "data.propertyInfo." "summary.location." "staticImage.url",
                        response,
                    )

                    return details.extend(
                        [(parsed_name, parsed_address, parsed_static_img)]
                    )

            raise PermissionError
        raise PermissionError

    except PermissionError:
        return False


if __name__ == "__main__":
    resp = asyncio.run(
        post_detail_request(
            hotel="74633678",
            photo_amt=15,
        )
    )
    print(resp)
