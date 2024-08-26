from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def create_greeting_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Привет"))
    builder.add(KeyboardButton(text="Пока"))
    builder.add(KeyboardButton(text="Меню"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def create_links_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Новости", callback_data="news"))
    builder.add(InlineKeyboardButton(text="Музыка", callback_data="music"))
    builder.add(InlineKeyboardButton(text="Видео", callback_data="video"))
    builder.adjust(1)
    return builder.as_markup()

def create_dynamic_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Показать больше", callback_data="show_more"))
    return builder.as_markup()

def create_options_keyboard(option_type):
    builder = InlineKeyboardBuilder()
    if option_type == "news":
        builder.add(InlineKeyboardButton(text="Вот список новостей", url="https://habr.com/ru/companies/cloud4y/articles/"))

    elif option_type == "music":
        builder.add(InlineKeyboardButton(text="Вот плей-лист музыки", url="https://pixabay.com/ru/music/battle-of-the-dragons-8037/"))

    elif option_type == "video":
        builder.add(InlineKeyboardButton(text="Вот список роликов", url="https://videos.pexels.com/video-files/1409899/1409899-uhd_2560_1440_25fps.mp4"))
    builder.add(InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu"))
    return builder.as_markup()

def create_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu"))
    return builder.as_markup()
