import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import Router
import requests
import config

# Логирование для отслеживания работы бота
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=config.TOKEN)
dp = Dispatcher()

router = Router()
dp.include_router(router)

# Клавиатура для ввода города
city_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Введите город")]
    ],
    resize_keyboard=True
)


# Функция получения погоды
def get_weather(city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={config.WEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# Хендлер для команды /start
@router.message(Command("start"))
async def start_command(message: types.Message):
    user_name = message.from_user.first_name
    await message.reply(
        f"Привет, {user_name}! Я бот, который может показать погоду. Нажмите на кнопку ниже и введите город.",
        reply_markup=city_keyboard)


# Хендлер для команды /help
@router.message(Command("help"))
async def help_command(message: types.Message):
    await message.reply(
        "Напишите название города, чтобы узнать текущую погоду. Используйте команду /start для перезапуска бота.")


# Хендлер для команды /city или ввода названия города
@router.message(Command("city"))
async def city_command(message: types.Message):
    await message.reply("Введите название города:")


@router.message(F.text)
async def get_city_weather(message: types.Message):
    city_name = message.text
    weather_data = get_weather(city_name)

    if weather_data:
        city = weather_data["name"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        pressure = weather_data["main"]["pressure"]
        await message.reply(
            f"В городе {city} температура - {temperature}°C\nВлажность воздуха - {humidity}%\nАтмосферное давление - {pressure} мм рт. ст.")
    else:
        await message.reply(
            "Не удалось найти погоду для указанного города. Пожалуйста, проверьте правильность написания города.")


# Запуск бота
if __name__ == "__main__":
    dp.run_polling(bot)
