from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.forms import LeaveForm
import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()
API_URL = os.getenv('API_URL')

def register_leave_handlers(dp: Dispatcher):
    @dp.message(Command('leave'))
    async def start_leave(message: types.Message, state: FSMContext):
        await state.set_state(LeaveForm.DATE)
        await message.reply("Darsdan ozodlik so‘rash uchun:\n1. Sana (YYYY-MM-DD):")

    @dp.message(LeaveForm.DATE)
    async def leave_date(message: types.Message, state: FSMContext):
        await state.update_data(date=message.text)
        await state.set_state(LeaveForm.REASON)
        await message.reply("2. Sabab:")

    @dp.message(LeaveForm.REASON)
    async def leave_reason(message: types.Message, state: FSMContext):
        data = await state.get_data()
        data['reason'] = message.text
        payload = {
            'student_phone': str(message.from_user.id),
            'date': data['date'],
            'reason': data['reason']
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL + "leave/request/", json=payload) as resp:
                if resp.status == 201:
                    await message.reply("Arizangiz yuborildi.")
                else:
                    await message.reply("Xatolik yuz berdi.")
        await state.clear()