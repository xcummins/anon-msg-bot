# handlers.py

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from main import dp, db
import random
import string

class Form(StatesGroup):
    waiting_for_referral_code = State()
    waiting_for_message = State()

@dp.message_handler(Command('start'))
async def cmd_start(message: types.Message):
    try:
        referral_code = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        db.add_user(message.from_user.id, referral_code)
        await message.reply(f"Welcome to Anon Message Bot!\nYour referral link is: /anon_{referral_code}")
    except Exception as e:
        await message.reply("An error occurred. Please try again.")
        logging.error(f"Error in cmd_start: {e}")

@dp.message_handler(Command('anon_'), state='*')
async def cmd_anon(message: types.Message):
    referral_code = message.text.split('_')[1]
    recipient_id = db.get_user_by_referral_code(referral_code)
    if recipient_id:
        await Form.waiting_for_message.set()
        await message.reply("Now send your anonymous message.")
        await Form.waiting_for_message.update_data(recipient_id=recipient_id[0])
    else:
        await message.reply("Invalid referral code.")

@dp.message_handler(state=Form.waiting_for_message)
async def process_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        recipient_id = data['recipient_id']
    db.save_message(message.from_user.id, recipient_id, message.text)
    await message.reply("Message sent anonymously!")
    await state.finish()

@dp.message_handler(Command('messages'))
async def cmd_messages(message: types.Message):
    messages = db.get_messages_for_user(message.from_user.id)
    if messages:
        for msg in messages:
            await message.reply(f"Message: {msg[0]}\nSent at: {msg[1]}")
    else:
        await message.reply("No messages yet.")