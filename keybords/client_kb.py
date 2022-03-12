from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def searched_markup(search_results_list):
    result_markup = InlineKeyboardMarkup(row_width=1)
    for i in range(len(search_results_list)):
        btn = InlineKeyboardButton(text=search_results_list[i], callback_data=f'search {i}')
        result_markup.add(btn)
    return result_markup