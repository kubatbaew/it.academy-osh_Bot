import asyncio
import datetime
from os import getenv

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext

from forms.form import request_name, FormCustomer, send_code
from routers.router import router

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

dp = Dispatcher()


@router.message(CommandStart())
async def command_start(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    try:
        data = await state.get_data()
        user_id = data['user_id']
    except KeyError:
        user_id = None

    if user_id == message.from_user.id:
        await send_code(message, state, bot)
    else:
        await state.set_state(FormCustomer.name)

        try:
            with open('templates/start.html', 'r', encoding='utf-8') as file:
                content = file.read()

            await bot.send_sticker(
                chat_id,
                'CAACAgIAAxkBAAELoQ5l6Y65LniM1iQrHs-vA7QyeecqtQACZwADQDHADXhtfVrKFwABjjQE'
            )
            await message.answer(content)
        except Exception as e:
            print(f"[ERROR]: {e}")

        await request_name(message)


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    print('[NOTIFICATION]: Start to Bot', datetime.datetime.now().strftime('%Y-%m-%d; %H:%M:%S'))
    asyncio.run(main())
