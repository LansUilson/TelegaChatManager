from aiogram.types import ChatType
from config import commands
from connector import dp, db, data
from aiogram import types

@dp.message_handler(commands=(['resetdb']), chat_type=ChatType.SUPERGROUP)
async def resdb(message: types.Message):
	await db.reset()
	await db.create_chat_default(message.chat.id)
	await message.answer("База данных пересоздана!")