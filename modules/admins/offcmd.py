from aiogram.types import ChatType
from config import commands, stng
from connector import dp, data
from aiogram import types
import utils

# Команда для выключения команд :| #
@dp.message_handler(gcm=(['^offcmd(?:(.+)|)$'], commands.offcmd), chat_type=ChatType.SUPERGROUP)
async def offcmd(message: types.Message, regexp_command):

	chatdata = data[message.chat.id*-1]

	if(not regexp_command.group(1)):

		msg = "Список активных и неактивных команд:\n"
		count = 0

		for i in chatdata['ofdcmds']:
			count+=1
			if(chatdata['ofdcmds'][i] == True):
				msg+=f"  {count}. {i} - неактивна\n"
			else:
				msg+=f"  {count}. {i} - активна\n"
			
		return await message.answer(msg)

	elif(regexp_command.group(1)):
		if(not regexp_command.group(1).lower()[1:] in stng.cmds):
			if(not chatdata['settings']['serror']): return await message.answer(f"Несуществующая команда. ({regexp_command.group(1)[1:]})")
			else: return False
		else:
			if(chatdata['ofdcmds'][regexp_command.group(1)[1:]] == True):
				chatdata['ofdcmds'][regexp_command.group(1)[1:]] = False
				active = "активна"
			else:
				chatdata['ofdcmds'][regexp_command.group(1)[1:]] = True
				active = "неактивна" 
			return await message.answer(f"Команда {regexp_command.group(1)[1:]} теперь {active}.")
