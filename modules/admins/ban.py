from config import commands, stng, rangs 
from connector import dp, bot, db, data
from aiogram.types import ChatType
from aiogram import types
import time
import utils

# Команда для бана пользователей #
@dp.message_handler(gcm=(['^ban(?:(?:( +(\d+)|)(?:( +(\d+)([a-zA-zА-яа-я]+)|)(?:( +([a-zA-zА-яа-я1-9?!.,:% ]+)|))|)))$'], commands.ban, True), chat_type=ChatType.SUPERGROUP)
async def welcome(message: types.Message, regexp_command):

	chatdata = data[message.chat.id*-1]
	user = await utils.getUser(chatdata['users'], message.from_user.id)

	if(not regexp_command.group(2)):
		if(not "reply_to_message" in str(message)):
			if(not chatdata['settings']['serror']): return await message.answer(f"Вы должны переслать сообщение или написать id ({settings[0]['prefix']}id) человека.")
			else: return False
		
		msg = message.reply_to_message['from']
		member = await utils.getUser(chatdata['users'], msg.id)
		if(not member): 
			if(not chatdata['settings']['serror']): return await message.answer("Данного пользователя нет в этом чате.")
			else: return False
	else:
		member = await utils.getUser(chatdata['users'], regexp_command.group(2))
		if(not member): 
			if(not chatdata['settings']['serror']): return await message.answer("Данного пользователя нет в этом чате.") 
			else: return False

		msg = { "id": regexp_command.group(2), "first_name": member['fname'], "last_name": member['lname'] } 

	if(not regexp_command.group(3)):
		date = ("forever", " навсегда")
	else:
		date = await utils.convert_time(regexp_command.group(4), regexp_command.group(5)) 
		
		if(not date): return await message.answer("Неизвестная дата.")
		if(date[0] > 504576000): return await message.answer("Максимально можно заблокировать пользователя на 16 лет.")

	if(member['id'] == message.from_user.id):
		if(not chatdata['settings']['serror']): return await message.answer("Вы не можете заблокировать самого себя.") 
		else: return False
	elif(member['rank'] == rangs.CREATOR):
		if(not chatdata['settings']['serror']): return await message.answer("Вы не можете заблокировать создателя чата.") 
		else: return False
	elif(member['rank'] >= user['rank']):
		if(not chatdata['settings']['serror']): return await message.answer("Данный пользователь выше или такого же ранга как Вы.") 
		else: return False

	reason = "."
	if(regexp_command.group(6)):
		if(len(regexp_command.group(6)) > 100):
			return await message.answer("Количество символов в причине не должно превышать 100.")
		reason = f" по причине:{regexp_command.group(6)}"

	if(str(msg['id']) in str(chatdata['banned'])):
		if(not chatdata['settings']['serror']): return await message.answer("Пользователь уже заблокирован.")
		else: return False

	await message.answer(text = f"Пользователь [{await utils.getName(msg)}](tg://user?id={msg['id']}) заблокирован в чате{date[1]}{reason}", parse_mode='Markdown', disable_notification = True)
	await bot.kick_chat_member(message.chat.id, msg['id'], time.time()+35)
	if(date[0] == "forever"):
		await db.ban(message.chat.id, msg['id'], 1, regexp_command.group(6))
	else:
		await db.ban(message.chat.id, msg['id'], time.time()+date[0], regexp_command.group(6))