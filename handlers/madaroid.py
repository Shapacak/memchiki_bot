import random
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data_base import sqldb


async def madaroid(message: types.Message):
    madara_rows = await sqldb.sql_view_mem_for_tag('мадара')
    mr = random.randrange(0,len(madara_rows))
    await message.answer_photo(madara_rows[mr][0])



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(madaroid, Text(startswith='мадара', ignore_case=True))
