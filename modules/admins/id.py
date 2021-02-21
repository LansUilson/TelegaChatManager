from aiogram.utils.markdown import pre
from aiogram.types import ChatType
from config import commands
from aiogram import types
from connector import dp
import utils

@dp.message_handler(gcm=(['^id$'], commands.id, True), chat_type=ChatType.SUPERGROUP)
async def stats(message: types.Message): 
	"""
	Receiving user ID EXCLUSIVE by reply message.
	"""

	if("reply_to_message" in str(message)):
		id = message.reply_to_message['from']
	else:
		id = message.from_user

	return await message.answer(f"ID пользователя [{await utils.getName(id)}](tg://user?id={id.id}): {pre(id.id)} (нажмите чтобы скопировать).", parse_mode='Markdown', disable_notification = True)