from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

load_btn = KeyboardButton('/Загрузить')
delete_btn = KeyboardButton('/Удалить')

admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

admin_keyboard.row(load_btn, delete_btn)