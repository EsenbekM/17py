from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import bot, ADMIN
from keyboards.client_kb import cancel_marcup
from database import bot_db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    surname = State()
    age = State()
    region = State()


async def fsm_start(message: types.Message):
    if message.chat.type == 'private':
        await FSMAdmin.photo.set()
        await bot.send_message(
            message.chat.id,
            f"Привет {message.from_user.full_name}, скинь фотку...",
            reply_markup=cancel_marcup
        )
    else:
        await message.answer("Пиши в личку!")


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['username'] = f"@{message.from_user.username}"
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer("Как тебя зовут?")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer("Какая фамилия?")


async def load_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await FSMAdmin.next()
    await message.answer("Скока лет??")


async def load_age(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['age'] = int(message.text)
        await FSMAdmin.next()
        await message.answer("Где живешь?")
    except:
        await message.answer("Только числа!!!")


async def load_region(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['region'] = message.text
    await bot_db.sql_command_insert(state)
    await state.finish()
    await message.answer("Все свободен)")


async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.reply("Регистрация отменена!")

async def delete_data(message: types.Message):
    if message.from_user.id == ADMIN:
        result = await bot_db.sql_command_all()
        for i in result:
            await bot.send_photo(message.from_user.id,
                                 i[2],
                                 caption=f"Name: {i[3]}\n"
                                         f"Surname: {i[4]}\n"
                                         f"Age: {i[5]}\n"
                                         f"Region: {i[6]}\n\n"
                                         f"{i[1]}\n",
                                 reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                     f"delete {i[3]}",
                                     callback_data=f'delete {i[0]}'
                                 ))
                                 )
    else:
        await message.answer("Ты не админ!!!")

async def complete_delete(call: types.CallbackQuery):
    await bot_db.sql_command_delete(call.data.replace('delete ', ''))
    await call.answer(text=f"{call.data.replace('delete ', '')} deleted", show_alert=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


def register_hendler_fsmanketa(dp: Dispatcher):
    dp.register_message_handler(cancel_registration, state='*', commands="cancel")
    dp.register_message_handler(cancel_registration,
                                Text(equals='cancel', ignore_case=True), state='*')

    dp.register_message_handler(fsm_start, commands=['register'])
    dp.register_message_handler(load_photo, state=FSMAdmin.photo, content_types=["photo"])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_surname, state=FSMAdmin.surname)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_region, state=FSMAdmin.region)
    dp.register_message_handler(delete_data, commands=["del"])
    dp.register_callback_query_handler(complete_delete,
                                       lambda call: call.data and
                                                    call.data.startswith("delete "))
