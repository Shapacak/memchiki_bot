from aiogram import executor
from create_bot import dp
from data_base import sqldb


async def on_startup(_):
    print('Бот в сети')
    sqldb.sql_connect_mems_db()

from handlers import client_wiki
from handlers import madaroid
from handlers import mems_admin


client_wiki.register_handlers_client(dp)
madaroid.register_handlers_client(dp)
mems_admin.register_handlers_admin(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)