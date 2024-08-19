from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# Создание Reply клавиатуры с кнопками "Привет", "Пока" и "Меню"
def create_greeting_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Привет"))
    builder.add(KeyboardButton(text="Пока"))
    builder.add(KeyboardButton(text="Меню"))
    builder.adjust(2)  # Равномерное распределение кнопок
    return builder.as_markup(resize_keyboard=True)

# Создание Inline клавиатуры с кнопками для новостей, музыки и видео
def create_links_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Новости", callback_data="option_1"))
    builder.add(InlineKeyboardButton(text="Музыка", callback_data="option_2"))
    builder.add(InlineKeyboardButton(text="Видео", callback_data="option_3"))
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

# Клавиатура для возврата в основное меню
def create_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu"))
    return builder.as_markup()

