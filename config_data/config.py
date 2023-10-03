import os
from dotenv import load_dotenv, find_dotenv
from peewee import SqliteDatabase
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE

if not find_dotenv():
    exit("Переменные окружения не загружены, т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("hello_world", "Приветственное сообщение"),
    ("help", "Вывести справку"),
    ("lowprice", "Топ самых дешевых отелей в городе"),
    ("highprice", "Топ самых дорогих отелей в городе"),
    ("bestdeal", "Топ предложений по запросу пользователя (цена/близость к центру)"),
    ('favorites', "Выдаёт избранные отели"),
    ("history", "История поиска отелей")
)

db = SqliteDatabase('hotel-bot.db')

CALENDAR = Calendar(RUSSIAN_LANGUAGE)
CALENDAR_CALLBACK = CallbackData("calendar", "action", "year", "month", "day")