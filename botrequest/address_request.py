import asyncio
import json
from typing import Any

import jmespath

from botrequest.api_request import api_request


async def post_address_request(hotel: str) -> Any:
    """Функция, обрабатывающая запрос адреса отеля"""

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
            check_errors = jmespath.search("errors", response)

            if check_errors is None:
                parsed_address = jmespath.search(
                    "data.propertyInfo.summary.location.address.addressLine",
                    response,
                )

                return parsed_address

        raise PermissionError

    except PermissionError:
        return False


if __name__ == "__main__":
    resp = asyncio.run(post_address_request(hotel="74633678"))
    print(resp)
