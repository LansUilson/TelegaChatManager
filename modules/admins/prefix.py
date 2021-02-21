from aiogram.types import ChatType
from config import commands, slist
from connector import dp, data
from aiogram import types
import utils

@dp.message_handler(gcm=(['^prefix(?:( +(.))|)$'], commands.prefix, True), chat_type=ChatType.SUPERGROUP)
async def unban(message: types.Message, regexp_command):

	chatdata = data[message.chat.id*-1]

	if(regexp_command.group(1)):
		if(regexp_command.group(1)[1:] in slist):
			chatdata['settings']['prefix'] = regexp_command.group(1)[1:]
			await message.answer(f"Префикс упешно изменён на {regexp_command.group(1)[1:]}")
		else: 
			if(not chatdata['settings']['serror']): await message.answer(f"Данного символа нет в белом списке. Список разрешённых символов:\n{slist}")
			else: return False
	else:
		return await message.answer(f"Префикс этого чата: {chatdata['settings']['prefix']}")