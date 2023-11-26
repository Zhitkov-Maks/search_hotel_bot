from typing import Any, Dict, Union, List

import aiohttp

from config import RAPIDAPI_KEY


async def api_request(
        method_endswith: str,
        params: Dict[str, Union[str, int, List, Dict]],
        method_type: str,
) -> Any:
    """Функция, определяющая тип API запроса"""

    url = f"https://hotels4.p.rapidapi.com/{method_endswith}"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    }

    if method_type == "GET":
        return await get_request(url=url, params=params, headers=headers)
    else:
        return await post_request(url=url, params=params, headers=headers)


async def get_request(url, params, headers):
    """Функция, обрабатывающая GET запрос"""

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(60)) as client:
        async with client.get(
                url=url, headers=headers, params=params, timeout=60
        ) as response:
            try:
                if response.status == 200:
                    return await response.text()

                raise PermissionError

            except PermissionError:
                return False


async def post_request(url, params, headers):
    """Функция, обрабатывающая POST запрос"""

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(60)) as client:
        async with client.post(
                url=url, headers=headers, json=params, timeout=60
        ) as response:
            try:
                if response.status == 200:
                    return await response.text()

                raise PermissionError

            except PermissionError:
                return False
