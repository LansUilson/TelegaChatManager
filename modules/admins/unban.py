from connector import dp, bot, db, data 
from aiogram.dispatcher import filters
from config import commands, rangs
from aiogram.types import ChatType
from aiogram import types
import utils

# Команда для разбана пользователей #
@dp.message_handler(gcm=(['^unban(?:(?:( +(\d+)|)|))$'], commands.unban, True), chat_type=ChatType.SUPERGROUP)
async def unban(message: types.Message, regexp_command):

	chatdata = data[message.chat.id*-1]

	if(not regexp_command.group(2)):
		if(not "reply_to_message" in str(message)):
			if(not chatdata['settings']['serror']): return await message.answer(f"Вы должны переслать сообщение или написать id ({settings[0]['prefix']}id) человека.")
			else: return False

		msg = message.reply_to_message['from'] 
		member = await utils.getUser(chatdata['users'], msg.id)
		if(len(member) == 0): 
			if(not chatdata['settings']['serror']): return await message.answer("Данного пользователя нет в этом чате.")
			else: return False
	else:
		member = await utils.getUser(chatdata['users'], regexp_command.group(2))
		if(len(member) == 0): 
			if(not chatdata['settings']['serror']): return await message.answer("Данного пользователя нет в этом чате.") 
			else: return False

		msg = { "id": regexp_command.group(2), "first_name": member['fname'], "last_name": member['lname'] } 

	if(not str(msg['id']) in str(banned)):
		if(not chatdata['settings']['serror']): return await message.answer("Пользователь не заблокирован.")
		else: return False

	await message.answer(text = f"Пользователь [{await utils.getName(msg)}](tg://user?id={msg['id']}) разблокирован.", parse_mode='Markdown', disable_notification = True)
	await db.unban(message.chat.id, msg['id'])
	await bot.unban_chat_member(message.chat.id, msg['id'])
