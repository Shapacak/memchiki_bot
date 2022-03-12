import sqlite3
from aiogram import types
from create_bot import bot


def sql_connect_mems_db():
    global base, cur
    base = sqlite3.connect('mems.db')
    if base:
        print('mems connected')
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS mems(img, name PRIMARY KEY, tag)')
    base.commit()


async def sql_add_mem(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO mems VALUES(?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_view_mems():
    rows = cur.execute('SELECT * FROM mems').fetchall()
    return rows

async def sql_view_mem_for_tag(tag):
    rows = cur.execute('SELECT img FROM mems WHERE tag == ?', (tag,)).fetchall()
    return rows

async def sql_delete_mem(mem_name):
    cur.execute('DELETE FROM mems WHERE name == ?', (mem_name,))
    base.commit()