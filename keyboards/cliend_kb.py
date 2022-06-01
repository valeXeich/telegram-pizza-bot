from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b_menu = KeyboardButton('/Меню')
b_geo = KeyboardButton('/Расположение')
b_time = KeyboardButton('/Режим_работы')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b_menu).add(b_geo).insert(b_time)

