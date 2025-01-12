# admin.py

from aiogram import types
from aiogram.dispatcher.filters import Command
from bot import dp, db, bot
from config import ADMIN_ID

@dp.message_handler(Command('admin'), user_id=ADMIN_ID)
async def cmd_admin(message: types.Message):
    await message.reply("Admin panel. Use /send_all to send a message to all users.")

@dp.message_handler(Command('send_all'), user_id=ADMIN_ID)
async def cmd_send_all(message: types.Message):
    await message.reply("Send a message to all users. Type your message now.")
    await dp.current_state(user=message.from_user.id).set_state('waiting_for_global_message')

@dp.message_handler(state='waiting_for_global_message', user_id=ADMIN_ID)
async def process_global_message(message: types.Message):
    users = db.cursor.execute("SELECT user_id FROM users").fetchall()
    for user_id in users:
        await bot.send_message(user_id[0], message.text)
    await message.reply("Message sent to all users.")
    await dp.current_state(user=message.from_user.id).finish()