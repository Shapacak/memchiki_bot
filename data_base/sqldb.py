import sqlite3
from aiogram import types
from create_bot import bot


def sql_connect_mems_db():
    global base, cur
    base = sqlite3.connect('data_base/mems.db')
    if base:
        print('mems connected')
    cur = base.cursor()
    create_tables()


def create_tables():
    with open('data_base/create_table.sql', 'r') as sql_commands:
        sql_script = sql_commands.read()
    base.executescript(sql_script)
    base.commit()
    print('Таблицы созданы')


async def sql_add_tag(state):
    async with state.proxy() as data:
        tag_name = tuple(data.values())
    print(tag_name)
    cur.execute('INSERT INTO tags(tag_name) VALUES(?)', tag_name)
    base.commit()


async def sql_view_tags():
    rows = cur.execute('SELECT tag_name FROM tags').fetchall()
    return rows


async def sql_delete_tag(tag_name):
    cur.execute('DELETE FROM tags WHERE tag_name == ?', (tag_name,))


async def sql_add_mem(state):
    async with state.proxy() as data:
        img, name, tag_name = tuple(data.values())
    cur.execute('''INSERT INTO mems(img,name,tag_id) 
                    SELECT ?, ?, (SELECT id FROM tags WHERE tag_name == ?)''', (img,name,tag_name,))
    base.commit()


async def sql_view_mems():
    rows = cur.execute('''SELECT img, name, tag_name
                            FROM mems INNER JOIN tags
                            ON mems.tag_id = tags.id''').fetchall()
    return rows


async def sql_view_random_mem():
    row = cur.execute('SELECT img FROM mems ORDER BY random() LIMIT 1').fetchall()
    return row


async def sql_view_random_mem_for_tag(tag):
    row = cur.execute('''SELECT img 
                            FROM mems INNER JOIN tags
                            ON tag_name == ? ORDER BY random() LIMIT 1''', (tag,)).fetchall()
    return row


async def sql_delete_mem(mem_name):
    cur.execute('DELETE FROM mems WHERE name == ?', (mem_name,))
    base.commit()