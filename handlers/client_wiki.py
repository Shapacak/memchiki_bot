import random

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keybords import searched_markup
from utils import wiki_util
from data_base import sqldb


class Wiki:
    titles_list = []
    prepared_summary = []
    splited_chunk = []

    @staticmethod
    def split_chunk(chunk):
        for i in range(0, len(chunk), 1400):
            Wiki.splited_chunk.append(chunk[i:i + 1400])


async def wiki_search(message: types.Message):
    query_string = message.text.split(' ', maxsplit=1)[1]
    Wiki.titles_list = wiki_util.search(query_string)
    if Wiki.titles_list:
        await message.delete()
        await message.answer(text=query_string, reply_markup=searched_markup(Wiki.titles_list))
    else:
        ponasenko_rows = await sqldb.sql_view_mem_for_tag('понасенко')
        pr = random.randrange(0, len(ponasenko_rows))
        await message.answer(text=f'По запросу "{message.text}" ничего не найдено, кусок ты кожанного мешка')
        await message.answer_photo(ponasenko_rows[pr][0])


async def summary_for_selected_search(callback: types.CallbackQuery):
    pre_summary = wiki_util.summary(Wiki.titles_list[int(callback.data.split(' ')[1])])
    Wiki.prepared_summary = pre_summary.split('\n\n\n')
    if len(Wiki.prepared_summary[0]) < 1400:
        await callback.message.answer(Wiki.prepared_summary.pop(0),
                                      reply_markup=InlineKeyboardMarkup().
                                      add(InlineKeyboardButton(text='Далее?',callback_data='nextchunk')))
        await callback.answer()
    else:
        Wiki.split_chunk(Wiki.prepared_summary.pop(0))
        await callback.message.answer(Wiki.splited_chunk.pop(0),
                                      reply_markup=InlineKeyboardMarkup().
                                      add(InlineKeyboardButton(text='Далее?', callback_data='nextsplitchunk')))
        await callback.answer()


async def next_chunk_summary(callback: types.CallbackQuery):
    if Wiki.prepared_summary:
        if len(Wiki.prepared_summary[0]) < 1400:
            await callback.message.answer(Wiki.prepared_summary.pop(0),
                                          reply_markup=InlineKeyboardMarkup().
                                          add(InlineKeyboardButton(text='Далее?', callback_data=f'nextchunk')))
            await callback.answer()
        else:
            Wiki.split_chunk(Wiki.prepared_summary.pop(0))
            await callback.message.answer(Wiki.splited_chunk.pop(0),
                                          reply_markup=InlineKeyboardMarkup().
                                          add(InlineKeyboardButton(text='Далее?', callback_data='nextsplitchunk')))
            await callback.answer()
    await callback.answer()


async def splited_chunk_summary(callback: types.CallbackQuery):
    if len(Wiki.splited_chunk) > 1:
        await callback.message.answer(Wiki.splited_chunk.pop(0),
                                      reply_markup=InlineKeyboardMarkup().
                                      add(InlineKeyboardButton(text='Далее?', callback_data='nextsplitchunk')))
        await callback.answer()
    else:
        await callback.message.answer(Wiki.splited_chunk.pop(0),
                                      reply_markup=InlineKeyboardMarkup().
                                      add(InlineKeyboardButton(text='Далее?', callback_data='nextchunk')))
        await callback.answer()




def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(wiki_search, Text(startswith='вики', ignore_case=True))
    dp.register_callback_query_handler(summary_for_selected_search, Text(startswith='search '))
    dp.register_callback_query_handler(next_chunk_summary, Text(startswith='nextchunk'))
    dp.register_callback_query_handler(splited_chunk_summary, Text(startswith='nextsplitchunk'))