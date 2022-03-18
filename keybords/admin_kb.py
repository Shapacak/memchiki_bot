from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

load_btn = KeyboardButton('/Загрузить')
delete_btn = KeyboardButton('/Удалить')
hi_btn = KeyboardButton('Привет')

admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

admin_keyboard.row(load_btn, delete_btn, hi_btn)

async def get_tag_select_kb(tags_list):
    tags_select_keyboard = InlineKeyboardMarkup(row_width=1)
    for i in tags_list:
        btn = InlineKeyboardButton(text=i[0], callback_data=f'tag {i[0]}')
        tags_select_keyboard.add(btn)
    return tags_select_keyboard