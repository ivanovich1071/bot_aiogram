import logging
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from keyboards import create_greeting_keyboard, create_links_keyboard, create_dynamic_keyboard, create_options_keyboard
import config

# Логирование для отслеживания работы бота
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=config.TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

@router.message(CommandStart())
async def send_welcome(message: Message):
    await message.answer("Выберите опцию:", reply_markup=create_greeting_keyboard())

@router.message(lambda message: message.text in ["Привет", "Пока"])
async def handle_greeting(message: Message):
    if message.text == "Привет":
        await message.answer(f"Привет, {message.from_user.first_name}!")
    elif message.text == "Пока":
        await message.answer(f"До свидания, {message.from_user.first_name}!")

@router.message(Command(commands=['links']))
async def send_links(message: Message):
    await message.answer("Выберите ссылку:", reply_markup=create_links_keyboard())

@router.message(Command(commands=['dynamic']))
async def send_dynamic(message: Message):
    await message.answer("Динамическое меню:", reply_markup=create_dynamic_keyboard())

@router.callback_query(lambda call: call.data == "show_more")
async def show_more_options(callback_query: CallbackQuery):
    await callback_query.message.edit_reply_markup(reply_markup=create_options_keyboard())

@router.callback_query(lambda call: call.data in ["option_1", "option_2"])
async def handle_option_selection(callback_query: CallbackQuery):
    selection = "Опция 1" if callback_query.data == "option_1" else "Опция 2"
    await callback_query.message.answer(f"Вы выбрали: {selection}")

async def main():
    # Запуск бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

