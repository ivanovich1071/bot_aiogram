import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram import F, Router
import requests
import config
import os
from gtts import gTTS
from googletrans import Translator

# Логирование для отслеживания работы бота
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=config.TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Создание папки img для сохранения изображений, если она не существует
if not os.path.exists("img"):
    os.makedirs("img")

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
async def start_command(message: types.Message):
    user_name = message.from_user.first_name
    await message.reply(
        f"Привет, {user_name}! Я бот, который может показать погоду. Нажмите на кнопку ниже и введите город.",
        reply_markup=city_keyboard
    )

# Хендлер для команды /help
@router.message(Command("help"))
async def help_command(message: types.Message):
    await message.reply(
        "Напишите название города, чтобы узнать текущую погоду. Используйте команду /start для перезапуска бота."
    )

# Хендлер для команды /city
@router.message(Command("city"))
async def city_command(message: types.Message):
    await message.reply("Введите название города:")

# Хендлер для получения и отправки погоды с изображением и голосовым сообщением
@router.message(F.text & ~F.text.startswith("/"))
async def get_city_weather(message: types.Message):
    city_name = message.text
    weather_data = get_weather(city_name)

    if weather_data:
        city = weather_data["name"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        pressure = weather_data["main"]["pressure"]

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
            full_image_path = os.path.join(os.path.dirname(__file__), image_path)
            if os.path.exists(full_image_path):
                try:
                    photo = FSInputFile(full_image_path)
                    await message.answer_photo(photo=photo)
                except Exception as e:
                    await message.reply(f"Произошла ошибка при отправке изображения: {e}")

        await message.reply(weather_text)
    else:
        await message.reply(
            "Не удалось найти погоду для указанного города. Пожалуйста, проверьте правильность написания города."
        )

# Хендлер для команды /translate
@router.message(Command("translate"))
async def translate_command(message: types.Message):
    await message.reply("Введите текст для перевода:")

# Хендлер для перевода текста
@router.message(F.text & F.text.startswith("/translate"))
async def translate_text(message: types.Message):
    translator = Translator()
    text_to_translate = message.text.replace("/translate", "").strip()
    if text_to_translate:
        translated_text = translator.translate(text_to_translate, dest='en').text
        await message.reply(f"Перевод: {translated_text}")
    else:
        await message.reply("Пожалуйста, введите текст для перевода после команды /translate.")

# Хендлер для получения и сохранения изображений от пользователя
@router.message(F.photo)
async def handle_photo(message: types.Message):
    photo_id = message.photo[-1].file_id
    file_info = await bot.get_file(photo_id)
    destination = f"img/{photo_id}.jpg"
    await bot.download_file(file_info.file_path, destination)
    await message.reply_photo(photo=photo_id, caption="Вы отправили фото")

# Запуск бота
if __name__ == "__main__":
    dp.run_polling(bot)
