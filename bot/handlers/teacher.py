from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.forms import TeacherForm
import aiohttp
from decouple import config

API_URL = config('API_URL', default='http://127.0.0.1:8000/api/')

def register_teacher_handlers(dp: Dispatcher):
    @dp.message(Command('teacher'))
    async def start_teacher(message: types.Message, state: FSMContext):
        await state.set_state(TeacherForm.SUBJECT)
        await message.reply("O‘qtuvchi sifatida ro‘yxatdan o‘tish uchun:\n1. Fan:")

    @dp.message(TeacherForm.SUBJECT)
    async def teacher_subject(message: types.Message, state: FSMContext):
        await state.update_data(subject=message.text)
        await state.set_state(TeacherForm.NAME)
        await message.reply("2. Ism va familiyangiz:")

    @dp.message(TeacherForm.NAME)
    async def teacher_name(message: types.Message, state: FSMContext):
        await state.update_data(name=message.text)
        await state.set_state(TeacherForm.PHONE)
        await message.reply("3. Telefon raqamingiz (+998901234567):")

    @dp.message(TeacherForm.PHONE)
    async def teacher_phone(message: types.Message, state: FSMContext):
        data = await state.get_data()
        data['phone'] = message.text
        payload = {
            'subject': data['subject'],
            'name': data['name'],
            'phone': data['phone']
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL + "teacher/register/", json=payload) as resp:
                if resp.status == 201:
                    await message.reply("Arizangiz qabul qilindi! Admin bog‘lanadi.")
                else:
                    await message.reply("Xatolik yuz berdi.")
        await state.clear()