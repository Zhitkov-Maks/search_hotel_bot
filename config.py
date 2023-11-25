from decouple import config

BOT_TOKEN = config('TOKEN')
RAPIDAPI_KEY = config("RAPIDAPI_KEY")

text = """Список доступных команд: 
/lowprice - Вывод самых дешёвых отелей.
/highprice - Вывод самых дорогих отелей.
/bestdeal - Вывод отелей, наиболее подходящих по цене и расположению от центра.
/history - Вывод истории поиска отелей."
/money - В какой валюте будем искать отели?"""

list_base_command = [
    "/bestdeal",
    "/help",
    "/start",
    "/lowprice",
    "/highprice",
    "/money",
    "/history"
]
