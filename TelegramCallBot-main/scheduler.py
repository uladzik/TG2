# scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
scheduler = AsyncIOScheduler()

async def send_reminder(chat_id, text):
    await bot.send_message(chat_id, f"🔔 Напоминание: {text}")

def schedule_reminder(chat_id, run_dt, text):
    scheduler.add_job(send_reminder, "date", run_date=run_dt, args=[chat_id, text])

def start_scheduler():
    scheduler.start()

