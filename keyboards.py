
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# Создание Reply клавиатуры с кнопками "Привет" и "Пока"
def create_greeting_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Привет"))
    builder.add(KeyboardButton(text="Пока"))
    builder.adjust(2)  # Равномерное распределение кнопок
    return builder.as_markup(resize_keyboard=True)

# Создание Inline клавиатуры с кнопками для новостей, музыки и видео
def create_links_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Новости", url="https://habr.com/ru/companies/cloud4y/articles/"))
    builder.add(InlineKeyboardButton(text="Музыка", url="https://pixabay.com/ru/music/battle-of-the-dragons-8037/"))
    builder.add(InlineKeyboardButton(text="Видео", url="https://videos.pexels.com/video-files/1409899/1409899-uhd_2560_1440_25fps.mp4 "))
    builder.adjust(1)  # Все кнопки в одном ряду
    return builder.as_markup()

# Создание динамической Inline клавиатуры с кнопкой "Показать больше"
def create_dynamic_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Показать больше", callback_data="show_more"))
    return builder.as_markup()

# Функция для изменения клавиатуры при нажатии "Показать больше"
def create_options_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="просмотреть все", callback_data="option_1"))
    builder.add(InlineKeyboardButton(text="вернутся", callback_data="option_2"))
    builder.adjust(1)  # Кнопки в одном ряду
    return builder.as_markup()
