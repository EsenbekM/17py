from aiogram import types, Dispatcher
from config import bot, dp
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from keyboards import client_kb
from database.bot_db import sql_command_random

# @dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f"Привет мой хозяин {message.from_user.full_name}",
                         reply_markup=client_kb.start_markup)


async def help(message: types.Message):
    await message.answer(f"ННСТРУКЦИЯ")


# @dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("NEXT", callback_data="button_call_1")
    markup.add(button_call_1)

    question = "Сколько будет 1 + 1 ?"
    answers = ['1', '2', '3', '4', '322']
    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation="Это же легко",
        explanation_parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=markup
    )

async def show_random_user(message: types.Message):
    await sql_command_random(message)

def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help, commands=['help'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(show_random_user, commands=['random'])
