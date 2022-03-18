from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from keybords import  select_difficult_kb
from utils import brain_make


async def brain_go(message: types.Message):
    await message.answer('Выберите сложность', reply_markup=select_difficult_kb)


async def brain_start(callback: types.CallbackQuery):
    await callback.message.delete()
    difficult = callback.data.split(' ')[1]
    image = await brain_make(difficult)
    await callback.message.answer_photo(image)
    await callback.answer()


def register_handlers_brainer(dp: Dispatcher):
    dp.register_message_handler(brain_go, Text(startswith='brain', ignore_case=True))
    dp.register_callback_query_handler(brain_start, Text(startswith='difficult'))