from aiogram.dispatcher import filters
from config import commands, rangs
from aiogram.types import ChatType
from connector import dp, bot, data
from aiogram import types
import time
import utils

@dp.message_handler(gcm=(['^kick(?:(?:( +(\d+)|)(?:( +(.+)|))|))$'], commands.kick, True), chat_type=ChatType.SUPERGROUP)
async def kick(message: types.Message, regexp_command):
	""" Удаление пользователя из чата """

	chatdata = data[message.chat.id*-1]
	user = await utils.getUser(chatdata['users'], message.from_user.id)

	if(regexp_command.group(2) == None):
		if("reply_to_message" in str(message)):
			msg = message.reply_to_message['from']
		else:
			if(not settings[0]['serror']): return await message.answer(f"Вы должны переслать сообщение или написать id ({settings[0]['prefix']}id) человека.")
			else: return False

		member = await utils.getUser(chatdata['users'], msg.id)
		if(len(member) == 0): 
			if(not settings[0]['serror']): return await message.answer("Данного пользователя нет в этом чате.")
			else: return False

	else:
		member = await utils.getUser(chatdata['users'], regexp_command.group(2))
		if(len(member) == 0): 
			if(not settings[0]['serror']): return await message.answer("Данного пользователя нет в этом чате.") 
			else: return False

		msg = { "id": regexp_command.group(2), "first_name": member['fname'], "last_name": member['lname'] } 

	if(member['id'] == message.from_user.id):
		if(not settings[0]['serror']): return await message.answer("Вы не можете кикнуть самого себя.") 
		else: return False
	elif(member['rank'] == rangs.CREATOR):
		if(not settings[0]['serror']): return await message.answer("Вы не можете кикнуть создателя чата.") 
		else: return False
	elif(member['rank'] >= user['rank']):
		if(not settings[0]['serror']): return await message.answer("Данный пользователь выше или такого же ранга как Вы.") 
		else: return False

	cont = "."
	if(not regexp_command.group(4)):
		if(len(regexp_command.group(4)) > 100):
			return await message.answer("Количество символов в причине не должно превышать 100.")
		cont = f" по причине: {regexp_command.group(4)}"

	await message.answer(text = f"Пользователь [{await utils.getName(msg)}](tg://user?id={msg['id']}) исключён из чата{cont}", parse_mode='Markdown', disable_notification = True)
	await bot.kick_chat_member(message.chat.id, msg['id'], time.time()+35)
