import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
from aiogram import Router
import requests
import config
from googletrans import Translator  # Импортируем Translator для перевода текста

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
        [KeyboardButton(text="Введите текст")]
    ],
    resize_keyboard=True
)



# Хендлер для команды /start
@router.message(Command("start"))
async def start_command(message: types.Message):
    user_name = message.from_user.first_name
    await message.reply(
        f"Привет, {user_name}! Я бот, который может переводит текст. ",
        reply_markup=city_keyboard
    )

# Хендлер для команды /help
@router.message(Command("help"))
async def help_command(message: types.Message):
    await message.reply(
        "Напишите название города, чтобы узнать текущую погоду. Используйте команду /start для перезапуска бота."
    )

# Хендлер для команды /translate
@router.message(Command("translate"))
async def translate_command(message: types.Message):
    await message.reply("Введите текст для перевода:")

# Хендлер для перевода текста
@router.message(F.text & ~F.text.startswith("/"))
async def handle_text_message(message: types.Message):
    translator = Translator()
    text_to_translate = message.text.strip()
    translated_text = translator.translate(text_to_translate, dest='en').text
    await message.reply(f"Перевод: {translated_text}")



# Запуск бота
if __name__ == "__main__":
    dp.run_polling(bot)
