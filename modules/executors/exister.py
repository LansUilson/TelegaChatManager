from aiogram.types import ChatType
from connector import dp, data
from aiogram import types
from config import rangs
import math
import utils

# Обновление статистики левела, експы, сообщений и т.д #
@dp.message_handler(chat_type=ChatType.SUPERGROUP, not_command=False)
async def existAndLevels(message: types.Message):

	chatdata = data[message.chat.id*-1]
	if(not utils.checkExist(message.from_user.id, chatdata)): await utils.createDefaultUser(message)

	user = await utils.getUser(chatdata['users'], message.from_user.id)
	chat = chatdata['chat']

	if(chat['lastsender'] != message.from_user.id):

		chat['lastsender'] = message.from_user.id
		chat['mess'] = chat['mess']+1
		chat['messncons'] = chat['messncons']+1

		user['mess'] = user['mess']+1
		user['messncons'] = user['messncons']+1

		if(round(user['exp']) >= user['needexp']):
			user['level'] += 1
			user['exp'] = user['exp']-user['needexp'] 
			user['needexp'] = (50*math.pow(1.1, user['level'])) 
			await message.answer(f"{message.from_user.first_name} {message.from_user.last_name} поднял(а) уровень. Теперь у него(её) {user['level']} левел!")
		else:
			user['exp'] += 0.5 

		if(chat['exp'] >= chat['needexp']):
			chat['level'] += 1
			chat['exp'] = chat['exp']-chat['needexp']
			chat['needexp'] = (182*math.pow(1.1, chat['level'])) 
			await message.answer(f"Поздравляем! Ваш чат теперь {chat['level']} уровня!")
		else:
			chat['exp'] += 0.5

	else:
		user['mess'] = user['mess']+1
		chat['mess'] = chat['mess']+1
