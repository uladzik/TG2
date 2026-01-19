import os
from dotenv import load_dotenv
load_dotenv()

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
import asyncio
from scheduler import start_scheduler

TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    print("❌ BOT_TOKEN not set! Check Railway Variables.")
    exit(1)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📅 Open Calendar", web_app=WebAppInfo(url="https://my-call-calendar.vercel.app/"))]],
        resize_keyboard=True, one_time_keyboard=False
    )
    await message.answer("📅 Добро пожаловать!", reply_markup=kb)

async def main():
    print("🚀 Bot starting...")
    start_scheduler()
    print("📡 Polling...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())


