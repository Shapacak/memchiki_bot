from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


select_difficult_kb = InlineKeyboardMarkup(row_width=3)

easy_btn = InlineKeyboardButton(text='Легкая', callback_data='difficult easy')
medium_btn = InlineKeyboardButton(text='Средняя', callback_data='difficult medium')
hard_btn = InlineKeyboardButton(text='Тяжелая', callback_data='difficult hard')


select_difficult_kb.add(easy_btn, medium_btn, hard_btn)