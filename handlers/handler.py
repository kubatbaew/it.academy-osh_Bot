from aiogram import types

from forms.form import (
    request_phone_number,
    request_age,
    request_laptop,
    request_level,
    send_code,
)


async def handler_name(message: types.Message):
    await request_age(message)


async def handler_age(message: types.Message):
    await request_laptop(message)


async def handler_laptop(message: types.Message):
    await request_level(message)


async def handler_level(message: types.Message):
    await request_phone_number(message)


async def handler_phone_number(message: types.Message, state, bot):
    await send_code(message, state, bot, is_first=True)


async def wait_please(message: types.Message):
    mes_id = await message.answer(
        "<b>Ваша заявка отправляется...</b>⏳",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    return mes_id.message_id

