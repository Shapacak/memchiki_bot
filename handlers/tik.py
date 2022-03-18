from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.dispatcher.filters import Text


async def tik(message: types.Message):
    await message.answer('Тиk', reply_markup=InlineKeyboardMarkup().
                         add(InlineKeyboardButton(text='Изменить', callback_data='change')))


async def tak(callback: types.CallbackQuery):
    if callback.message.text == 'Так':
        msg = 'Тик'
    else:
        msg = 'Так'
    await callback.message.edit_text(msg, reply_markup=InlineKeyboardMarkup().
                         add(InlineKeyboardButton(text='Изменить', callback_data='change')))
    
    await callback.answer()


def register_handlers_tik_tak(dp: Dispatcher):
    dp.register_message_handler(tik, commands=['tik'])
    dp.register_callback_query_handler(tak, Text(startswith='change'))