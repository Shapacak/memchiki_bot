from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import dp, bot
from data_base import sqldb


class FSMMem(StatesGroup):
    photo = State()
    name = State()
    tag = State()


async def new_mem(message: types.Message):
    await FSMMem.photo.set()
    await message.reply('Загрузи фото')


async def cancel_states(message: types.Message, state: FSMContext):
    print(message.text)
    if not state.get_state():
        return
    await state.finish()
    await message.reply('ОК ЕБАНА')


async def mem_photo_load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
         data['photo'] = message.photo[0].file_id
    await FSMMem.next()
    await message.reply('Теперь введи название мема')


async def mem_name_enter(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMMem.next()
    await message.reply('Теперь введи тэг')


async def mem_tag_enter(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tag'] = message.text

    await sqldb.sql_add_mem(state)
    await message.reply('Добавлено')
    await state.finish()


async def delete_mem(message: types.Message):
    rows = await sqldb.sql_view_mems()
    for row in rows:
        await bot.send_photo(message.from_user.id, row[0], f'{row[1]}\n{row[2]}')
        await bot.send_message(message.from_user.id,text=f'Удалить {row[1]}?', reply_markup=InlineKeyboardMarkup().\
                               add(InlineKeyboardButton(text='Да', callback_data=f'del {row[1]}')))


async def delete_mem_callback(callback: types.CallbackQuery):
    await sqldb.sql_delete_mem(callback.data.replace('del ', ''))
    await callback.answer(f"{callback.data.replace('del ','')} был удален",show_alert=True)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(new_mem, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_states, state="*",commands=['Отмена'])
    dp.register_message_handler(cancel_states, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(mem_photo_load, content_types=['photo'], state=FSMMem.photo)
    dp.register_message_handler(mem_name_enter, state=FSMMem.name)
    dp.register_message_handler(mem_tag_enter, state=FSMMem.tag)
    dp.register_message_handler(delete_mem, commands=['Удалить'])
    dp.register_callback_query_handler(delete_mem_callback, lambda x: x.data and x.data.startswith('del '))