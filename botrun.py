import logging
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from keyboards import create_greeting_keyboard, create_links_keyboard, create_dynamic_keyboard, create_options_keyboard, create_menu_keyboard
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

@router.message(lambda message: message.text in ["Привет", "Пока", "Меню"])
async def handle_greeting(message: Message):
    if message.text == "Привет":
        await message.answer(f"Привет, {message.from_user.first_name}!")
    elif message.text == "Пока":
        await message.answer(f"До свидания, {message.from_user.first_name}!")
    elif message.text == "Меню":
        await message.answer("Выберите ссылку:", reply_markup=create_links_keyboard())

@router.message(Command(commands=['links']))
async def send_links(message: Message):
    await message.answer("Выберите ссылку:", reply_markup=create_links_keyboard())

@router.message(Command(commands=['dynamic']))
async def send_dynamic(message: Message):
    await message.answer("Динамическое меню:", reply_markup=create_dynamic_keyboard())

@router.callback_query(lambda call: call.data == "show_more")
async def show_more_options(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Выберите опцию:", reply_markup=create_options_keyboard())

@router.callback_query(lambda call: call.data in ["option_1", "option_2", "option_3", "back_to_menu"])
async def handle_option_selection(callback_query: CallbackQuery):
    if callback_query.data == "option_1":
        await callback_query.message.edit_text("Вот список новостей", reply_markup=create_menu_keyboard())
    elif callback_query.data == "option_2":
        await callback_query.message.edit_text("Вот плей-лист музыки", reply_markup=create_menu_keyboard())
    elif callback_query.data == "option_3":
        await callback_query.message.edit_text("Вот список роликов", reply_markup=create_menu_keyboard())
    elif callback_query.data == "back_to_menu":
        await callback_query.message.answer("Выберите опцию:", reply_markup=create_greeting_keyboard())

@router.message(lambda message: True)
async def unknown_message(message: Message):
    await message.answer("Извините, я не понимаю эту команду. Пожалуйста, выберите опцию из меню.", reply_markup=create_greeting_keyboard())

async def main():
    # Запуск бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
