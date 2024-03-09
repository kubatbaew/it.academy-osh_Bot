import asyncio

from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class FormCustomer(StatesGroup):
    user_id = State()
    name = State()
    age = State()
    laptop = State()
    level = State()
    phone_number = State()

    discount_token = State()
    created_at = State()


async def request_name(message: types.Message):
    await message.answer("<b>Как тебя зовут: </b>")


async def request_age(message: types.Message):
    await message.answer("<b>Сколько тебе лет: </b>")


async def request_laptop(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True, keyboard=[
            [
                types.KeyboardButton(text="Да"),
                types.KeyboardButton(text="Нет"),
            ]
        ]
    )
    await message.answer("<b>У тебя есть ноутбук? </b>", reply_markup=keyboard)


async def request_level(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True, keyboard=[
            [
                types.KeyboardButton(text="1"),
                types.KeyboardButton(text="2"),
                types.KeyboardButton(text="3"),
                types.KeyboardButton(text="4"),
                types.KeyboardButton(text="5"),
            ]
        ]
    )
    await message.answer("<b>Какой у тебя уровень знания программирования: </b>", reply_markup=keyboard)


async def request_phone_number(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
        [
            types.KeyboardButton(text="Отправить номер", request_contact=True)
        ]
    ])

    await message.answer("<b>Отправь свой номер: </b>",
                         reply_markup=keyboard)


async def send_code(message: types.Message, state: FSMContext, bot: Bot, is_first: bool = None):
    await state.update_data(user_id=message.from_user.id)
    data = await state.get_data()
    print(data)
    await state.set_state()

    if is_first:
        await bot.delete_message(chat_id=message.chat.id, message_id=data['wait_message_id'])

    with open('templates/end.html', "r", encoding='utf-8') as file:
        content = file.read()

    await bot.send_sticker(
        message.chat.id,
        sticker="CAACAgIAAxkBAAELoRll6Y_lMflBYJmMeyZTfgrjkYyXIAACaQADQDHADUw0nE7lxYF2NAQ"
    )
    await message.answer(content.format(data['discount_token']))

    await asyncio.sleep(600)

    with open('templates/happy.html', 'r', encoding='utf-8') as file:
        happy = file.read()

    await message.answer(happy)
