from aiogram.types import ChatType
from config import commands, stng
from connector import dp, data
from aiogram import types
import utils

# Команда для ищменения приветствия #
@dp.message_handler(gcm=(['^welcome(?:(.+)|)$'], commands.welcome, True), chat_type=ChatType.SUPERGROUP)
async def welcome(message: types.Message, regexp_command):

	chatdata = data[message.chat.id*-1]

	if(not regexp_command.group(1)):

		return await message.answer(f"Текст, который будет отправляться при вступлении нового участика в чат:\n{data[message.chat.id*-1]['settings']['welcome']}")

	elif(regexp_command.group(1)):
		if(len(regexp_command.group(1))>4000):
			if(not chatdata['settings']['serror']): return await message.answer("Длина сообщения для приветствия не должна превышать 4000 символов.")
			else: return False
		else:
			chatdata['settings']['welcome'] = regexp_command.group(1)[1:]
			return await message.answer(f"Сообщение для приветствия успешно установлено на\n\"{regexp_command.group(1)[1:]}\"")
