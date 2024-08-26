import logging
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from keyboards import create_greeting_keyboard, create_links_keyboard, create_dynamic_keyboard, create_options_keyboard, create_menu_keyboard
import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

@router.message(CommandStart())
async def send_welcome(message: Message):
    await message.answer("Привет! Я ваш бот. Выберите опцию из меню:", reply_markup=create_greeting_keyboard())

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

@router.callback_query(lambda call: call.data in ["news", "music", "video"])
async def handle_option_selection(callback_query: CallbackQuery):
    option_type = callback_query.data
    await callback_query.message.edit_text(f"Вы выбрали {option_type}.", reply_markup=create_options_keyboard(option_type))

@router.callback_query(lambda call: call.data == "show_more")
async def show_more_options(callback_query: CallbackQuery):
    await callback_query.message.edit_text("Выберите опцию:", reply_markup=create_options_keyboard("dynamic"))

@router.callback_query(lambda call: call.data == "back_to_menu")
async def back_to_menu(callback_query: CallbackQuery):
    # Вернуться в меню выбора "Новости/Музыка/Видео"
    await callback_query.message.edit_text("Выберите ссылку:", reply_markup=create_links_keyboard())

@router.message(lambda message: True)
async def unknown_message(message: Message):
    await message.answer("Извините, я не понимаю эту команду. Пожалуйста, выберите опцию из меню.", reply_markup=create_greeting_keyboard())

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
