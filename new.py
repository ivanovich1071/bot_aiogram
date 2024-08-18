import logging
import sqlite3
import os
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram import F, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from gtts import gTTS
import config

# Логирование для отслеживания работы бота
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=config.TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

# Создание базы данных SQLite
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        chat_id INTEGER PRIMARY KEY,
        registration_name TEXT,
        age INTEGER,
        registration_city TEXT,
        requested_cities TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# Определение состояний для регистрации
class RegistrationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_city = State()

# Клавиатура для регистрации
registration_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Начать регистрацию")]
    ],
    resize_keyboard=True
)

# Клавиатура для ввода города
city_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Введите город")]
    ],
    resize_keyboard=True
)

# Функция для получения погоды через асинхронный запрос
async def get_weather(city_name):
    async with aiohttp.ClientSession() as session:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={config.WEATHER_API_KEY}&units=metric&lang=ru"
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None

# Функция выбора изображения по температуре
def choose_image_by_temperature(temperature):
    if 20 <= temperature <= 50:
        return "photo/sonnycity.jpeg"
    elif -50 <= temperature < 0:
        return "photo/snowcity.jpeg"
    elif 0 <= temperature < 10:
        return "photo/raincity.jpeg"
    elif 10 <= temperature < 20:
        return "photo/springcity.jpeg"
    else:
        return None

# Функция для создания голосового сообщения
def create_voice_message(text, lang='ru'):
    tts = gTTS(text=text, lang=lang)
    voice_file_path = os.path.join("img", "voice_message.ogg")
    tts.save(voice_file_path)
    return voice_file_path

# Хендлер для команды /start
@router.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    await message.reply("Добро пожаловать! Давайте начнем регистрацию. Как вас зовут?", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(RegistrationStates.waiting_for_name)

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, chat_id) VALUES (?, ?) ON CONFLICT(chat_id) DO NOTHING", (username, message.chat.id))
    conn.commit()
    conn.close()

# Хендлер для регистрации имени
@router.message(RegistrationStates.waiting_for_name)
async def register_name(message: types.Message, state: FSMContext):
    name = message.text
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET registration_name = ? WHERE chat_id = ?", (name, message.chat.id))
    conn.commit()
    conn.close()
    await message.reply("Спасибо! Теперь укажите ваш возраст:")
    await state.set_state(RegistrationStates.waiting_for_age)

# Хендлер для регистрации возраста
@router.message(RegistrationStates.waiting_for_age)
async def register_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.reply("Пожалуйста, введите ваш возраст числом.")
        return
    age = int(message.text)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET age = ? WHERE chat_id = ?", (age, message.chat.id))
    conn.commit()
    conn.close()
    await message.reply("Отлично! Теперь укажите город, в котором вы проживаете:")
    await state.set_state(RegistrationStates.waiting_for_city)

# Хендлер для регистрации города
@router.message(RegistrationStates.waiting_for_city)
async def register_city(message: types.Message, state: FSMContext):
    city = message.text
    weather_data = await get_weather(city)
    if weather_data:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET registration_city = ? WHERE chat_id = ?", (city, message.chat.id))
        conn.commit()
        conn.close()

        # Приветствие и погода
        weather_text = (f"В городе {city} температура - {weather_data['main']['temp']}°C\n"
                        f"Влажность воздуха - {weather_data['main']['humidity']}%\n"
                        f"Атмосферное давление - {weather_data['main']['pressure']} мм рт. ст.")

        # Голосовое сообщение и изображение
        voice_message_path = create_voice_message(weather_text)
        image_path = choose_image_by_temperature(weather_data['main']['temp'])

        await message.reply(f"Регистрация завершена! Привет, {city}.")
        await message.reply_voice(voice=FSInputFile(voice_message_path))
        if image_path:
            await message.answer_photo(photo=FSInputFile(os.path.join(os.path.dirname(__file__), image_path)))
        await message.reply(weather_text, reply_markup=city_keyboard)
        await state.clear()  # Сбрасываем состояние после завершения регистрации
    else:
        await message.reply("Не удалось найти погоду для указанного города. Пожалуйста, попробуйте снова.")

# Хендлер для команды /city
@router.message(Command("city"))
async def city_command(message: types.Message):
    await message.reply("Введите название города:")

# Хендлер для получения и отправки погоды с изображением и голосовым сообщением
@router.message(lambda message: not message.text.startswith("/"))
async def get_city_weather(message: types.Message):
    city_name = message.text
    weather_data = await get_weather(city_name)

    if weather_data:
        city = weather_data["name"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        pressure = weather_data["main"]["pressure"]

        # Сохранение города в БД
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT requested_cities FROM users WHERE chat_id = ?", (message.chat.id,))
        cities = cursor.fetchone()[0]
        if cities:
            cities = cities + f", {city_name}"
        else:
            cities = city_name
        cursor.execute("UPDATE users SET requested_cities = ? WHERE chat_id = ?", (cities, message.chat.id))
        conn.commit()
        conn.close()

        weather_text = (f"В городе {city} температура - {temperature}°C\n"
                        f"Влажность воздуха - {humidity}%\n"
                        f"Атмосферное давление - {pressure} мм рт. ст.")

        # Создаем голосовое сообщение
        voice_message_path = create_voice_message(weather_text)

        # Отправка голосового сообщения
        await message.reply_voice(voice=FSInputFile(voice_message_path))

        # Выбор и отправка изображения в зависимости от температуры
        image_path = choose_image_by_temperature(temperature)
        if image_path:
            await message.answer_photo(photo=FSInputFile(os.path.join(os.path.dirname(__file__), image_path)))

        await message.reply(weather_text)
    else:
        await message.reply("Не удалось найти погоду для указанного города. Пожалуйста, проверьте правильность написания города.")

# Хендлер для команды /help
@router.message(Command("help"))
async def help_command(message: types.Message):
    await message.reply("Команда /start для регистрации и получения погоды.")

# Заглушка для команды /translate
@router.message(Command("translate"))
async def translate_command(message: types.Message):
    await message.reply("Функция перевода временно недоступна.")

# Заглушка для приема фото
@router.message(F.photo)
async def handle_photo(message: types.Message):
    await message.reply("Прием фото временно отключен.")

# Запуск бота
if __name__ == "__main__":
    dp.run_polling(bot)
