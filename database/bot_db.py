import sqlite3
import random
from config import bot

def sql_create():
    global db, cursor
    db = sqlite3.connect("bot.sqlite3")
    cursor = db.cursor()

    if db:
        print("База данных подключена!")
    db.execute("CREATE TABLE IF NOT EXISTS anketa "
               "(id INTEGER PRIMARY KEY, username TEXT,"
               "photo TEXT, name TEXT, surname TEXT,"
               "age INTEGER, region TEXT)")
    db.commit()

async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO anketa VALUES "
                       "(?, ?, ?, ?, ?, ?, ?)", tuple(data.values()))
        db.commit()

async def sql_command_random(message):
    result = cursor.execute("SELECT * FROM anketa").fetchall()
    random_user = random.randint(0, len(result) - 1)
    await bot.send_photo(message.from_user.id,
                         result[random_user][2],
                         caption= f"Name: {result[random_user][3]}\n"
                                   f"Surname: {result[random_user][4]}\n"
                                   f"Age: {result[random_user][5]}\n"
                                   f"Region: {result[random_user][6]}\n\n"
                                   f"{result[random_user][1]}\n")

async def sql_command_all():
    return cursor.execute("SELECT * FROM anketa").fetchall()

async def sql_command_delete(id):
    cursor.execute("DELETE FROM anketa WHERE id == ?", (id,))
    db.commit()
