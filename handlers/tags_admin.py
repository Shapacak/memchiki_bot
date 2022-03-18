from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types, Dispatcher
from create_bot import dp, bot
from data_base import sqldb


class FSMTag(StatesGroup):
    tag_name = State()


async def new_tag(message: types.Message):
    await FSMTag.tag_name.set()
    await bot.send_message(message.from_user.id, 'Введи имя тега')

async def cancel_states(message: types.Message, state: FSMContext):
    print(message.text)
    if not state.get_state():
        return
    await state.finish()
    await bot.send_message(message.from_user.id,'ОК ЕБАНА')

async def add_tag(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tag_name'] = message.text

    await sqldb.sql_add_tag(state)
    await bot.send_message(message.from_user.id, 'Тег добавлен')
    await state.finish()

async def delete_tag(message: types.Message):
    rows = await sqldb.sql_view_tags()
    for row in rows:
        await bot.send_message(message.from_user.id, text=f'Удалить тег {row[0]}?', reply_markup=InlineKeyboardMarkup(). \
                               add(InlineKeyboardButton(text='Да', callback_data=f'del {row[0]}')))


async def delete_tag_callback(callback: types.CallbackQuery):
    await sqldb.sql_delete_tag(callback.data.replace('del ', ''))
    await callback.answer(f"{callback.data.replace('del ', '')} был удален", show_alert=True)

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(new_tag, commands=['newtag'])
    dp.register_message_handler(cancel_states, state="*", commands=['cancel'])
    dp.register_message_handler(cancel_states, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(add_tag, state=FSMTag.tag_name)
    dp.register_message_handler(delete_tag, commands=['deletetag'])
    dp.register_callback_query_handler(delete_tag_callback, lambda x: x.data and x.data.startswith('del '))