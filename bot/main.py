import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.student import register_student_handlers
from handlers.teacher import register_teacher_handlers
from handlers.leave import register_leave_handlers
from handlers.payment import register_payment_handlers
from dotenv import load_dotenv
import os

# Logging sozlash
logging.basicConfig(level=logging.INFO)

# .env faylini yuklash
load_dotenv()

# Bot tokeni
API_TOKEN = os.getenv('API_TOKEN')

# Bot va dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def main():
    # Handlerlarni ro'yxatdan o'tkazish
    register_student_handlers(dp)
    register_teacher_handlers(dp)
    register_leave_handlers(dp)
    register_payment_handlers(dp)

    # Botni ishga tushirish
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
