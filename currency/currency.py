import requests

URL = "https://www.cbr-xml-daily.ru/daily_json.js"


async def get_valute() -> tuple:
    response = requests.get(url=URL)
    data = response.json()
    return (
        data.get('Valute').get("USD").get("Value"),
        data.get('Valute').get("EUR").get("Value"),
        data.get('Valute').get("BYN").get("Value"),
        data.get('Valute').get("CNY").get("Value"),
    )
