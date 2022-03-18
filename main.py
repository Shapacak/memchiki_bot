from aiogram import executor
from create_bot import dp
from data_base import sqldb


async def on_startup(_):
    print('Бот в сети')
    sqldb.sql_connect_mems_db()

from handlers import client_wiki
from handlers import memster
from handlers import brainer
from handlers import tik
from handlers import tags_admin
from handlers import mems_admin


client_wiki.register_handlers_client(dp)
memster.register_handlers_client(dp)
brainer.register_handlers_brainer(dp)
tik.register_handlers_tik_tak(dp)
tags_admin.register_handlers_admin(dp)
mems_admin.register_handlers_admin(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)