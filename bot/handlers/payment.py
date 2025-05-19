from aiogram import Dispatcher, types
from aiogram.filters import Command, ContentTypeFilter
from aiogram.fsm.context import FSMContext
from states.forms import PaymentForm
import aiohttp
from decouple import config

API_URL = config('API_URL', default='http://127.0.0.1:8000/api/')

def register_payment_handlers(dp: Dispatcher):
    @dp.message(Command('payment'))
    async def start_payment(message: types.Message, state: FSMContext):
        await state.set_state(PaymentForm.CHECK)
        await message.reply("To‘lov chekini rasm sifatida yuboring:")

    @dp.message(ContentTypeFilter(content_types=types.ContentType.PHOTO), PaymentForm.CHECK)
    async def payment_check(message: types.Message, state: FSMContext):
        photo = message.photo[-1].file_id
        payload = {
            'student_phone': str(message.from_user.id),
            'check': photo
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL + "payment/submit/", json=payload) as resp:
                if resp.status == 201:
                    await message.reply("Chek yuborildi. Tasdiqlanishini kuting.")
                else:
                    await message.reply("Xatolik yuz berdi.")
        await state.clear()