from config import commands, stng, slist
from aiogram.types import ChatType
from connector import dp, data
from aiogram import types
import utils

# Команда настроек для чата #
@dp.message_handler(gcm=(['^settings(?:((.+)( +([a-zA-Z]+|\d+)))|)$'], commands.settings, True), chat_type=ChatType.SUPERGROUP)
async def settings(message: types.Message, regexp_command):

	chatdata = data[message.chat.id*-1]

	if(not regexp_command.group(1)):

		offcmds=0
		for z in chatdata['ofdcmds']:
			if(chatdata['ofdcmds'][z]): offcmds+=1

		await message.answer(stng.stngs.format(chatdata['settings']['serror'], 
																					chatdata['settings']['prefix'], 
																					chatdata['settings']['autoreplace'], 
																					(chatdata['settings']['welcome'][:25] + '...') if len(chatdata['settings']['welcome']) > 25 else chatdata['settings']['welcome'], 
																					len(chatdata['ofdcmds'])-offcmds, 
																					len(chatdata['ofdcmds']))
												)

	elif(regexp_command.group(1)):
		if(regexp_command.group(3).lower()[1:] in stng.stngsbool):
			if(regexp_command.group(2).lower()[1:] == "true"):
				chatdata['settings'][regexp_command.group(3)[1:]] = True
			elif(regexp_command.group(2).lower()[1:] == "false"):
				chatdata['settings'][regexp_command.group(3)[1:]] = False
			else:
				if(not chatdata['settings']['serror']): return await message.answer("Неизвестное значение настройки.")
				else: return False
			return await message.answer(f"Настройка {regexp_command.group(3)[1:]} успешно изменена на {regexp_command.group(2)[1:]}.")

		if(regexp_command.group(3).lower()[1:] in stng.stngstr):
			if(regexp_command.group(3).lower()[1:] == "prefix"):
				if(regexp_command.group(2)[1:] in slist):
					chatdata['settings']['prefix'] = regexp_command.group(2)[1:]
					return await message.answer(f"Префикс упешно изменён на {regexp_command.group(1)[1:]}")
				else: 
					if(not chatdata['settings']['serror']): return await message.answer(f"Данного символа нет в белом списке. Список разрешённых символов:\n{slist}")
					else: return False
	
			elif("offcommand" in regexp_command.group(3).lower()[1:]):
				if(not chatdata['settings']['serror']): return await message.answer(f"Чтобы включить/отключить команду введите {chatdata['settings']['prefix']}offcmd [command].")
				else: return False
	
			elif("welcome" in regexp_command.group(3).lower()[1:]):
				if(len(regexp_command.group(2))>4000):
					if(not chatdata['settings']['serror']): return await message.answer("Длина сообщения для приветствия не должна превышать 4000 символов.")
					else: return False
				else:
					chatdata['settings']['welcome'] = regexp_command.group(2)[1:]
					return await message.answer(f"Сообщение для приветствия успешно установлено на\n\"{regexp_command.group(2)[1:]}\"")
