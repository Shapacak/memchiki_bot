import random
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from data_base import sqldb


async def madaroid(message: types.Message):
    print(message.from_user.id)
    madara_row = await sqldb.sql_view_random_mem_for_tag('мадара')
    await message.answer_photo(madara_row[0][0])

async def look_mem(message: types.Message):
    if len(message.text.split(' ')) > 1:
        tag = message.text.split(' ')[1]
        print(tag)
        mem = await sqldb.sql_view_random_mem_for_tag(tag)
        print(mem)
        await message.answer_photo(mem[0][0])
    else:
        mem = await sqldb.sql_view_random_mem()
        await message.answer_photo(mem[0][0])


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(madaroid, Text(startswith='мадара', ignore_case=True))
    dp.register_message_handler(look_mem, Text(startswith='мем', ignore_case=True))

