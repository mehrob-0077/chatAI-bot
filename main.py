from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from service import get_message, get_history, save_text, save_user
from connection import create_table
from dotenv import load_dotenv
import os
import asyncio


load_dotenv()

token = os.getenv("BOT_TOKEN")

bot = Bot(token)
dp = Dispatcher()


class AiRequest(StatesGroup):
    get_request = State()


@dp.message(Command("start"))
async def add_category(message: Message, state: FSMContext):

    await save_user(
        message.from_user.id,
        message.from_user.username
    )
    await message.answer("""Здрастувуйте!
Введите ваш запрос:""")
    await state.set_state(AiRequest.get_request)


@dp.message(AiRequest.get_request)
async def state_name_add(message: Message, state: FSMContext):

    history = await get_history(message.from_user.id)

    data = get_message(message.text, history)

    await save_text(message.from_user.id,message.text,data)

    await message.answer(data)


async def main():
    print("Bot started")
    await create_table()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())