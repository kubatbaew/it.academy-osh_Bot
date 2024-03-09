from datetime import datetime

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from forms.form import FormCustomer
from handlers.handler import (
    handler_age,
    handler_laptop,
    handler_level,
    handler_name,
    handler_phone_number,
    wait_please,
)
from utils.generate_discount_code import generate_code
from utils.google_sheets import add_user_to_sheets

router = Router()


@router.message(FormCustomer.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FormCustomer.age)
    await handler_name(message)


@router.message(FormCustomer.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(FormCustomer.laptop)
    await handler_age(message)


@router.message(FormCustomer.laptop)
async def process_laptop(message: types.Message, state: FSMContext):
    await state.update_data(laptop=message.text)
    await state.set_state(FormCustomer.level)
    await handler_laptop(message)


@router.message(FormCustomer.level)
async def process_level(message: types.Message, state: FSMContext):
    await state.update_data(level=message.text)
    await state.set_state(FormCustomer.phone_number)
    await handler_level(message)


@router.message(FormCustomer.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext, bot):
    wait_id = await wait_please(message)
    if message.contact:
        await state.update_data(phone_number=message.contact.phone_number)
    else:
        await state.update_data(phone_number=message.text)
    await state.update_data(created_at=datetime.now().strftime("%Y-%m-%d; %H:%M"))
    code = generate_code()
    await state.update_data(discount_token=code)
    add_user_to_sheets(await state.get_data())

    await state.update_data(wait_message_id=wait_id)

    await handler_phone_number(message, state, bot)
