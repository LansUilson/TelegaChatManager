from aiogram.dispatcher import filters
from config import commands, rangs
from aiogram.types import ChatType
from connector import dp, bot, data
from aiogram import types
import utils

@dp.message_handler(gcm=(['^unkick(?:(?:( +(\d+)|)|))$'], commands.unkick, True), chat_type=ChatType.SUPERGROUP)
async def unkick(message: types.Message, regexp_command):
	""" Разрешить пользователю заходить по ссылке после кика """

	chatdata = data[message.chat.id*-1]
	user = await utils.getUser(chatdata['users'], message.from_user.id)

	if(not regexp_command.group(2)):
		if(not "reply_to_message" in str(message)):
			if(not settings['serror']): return await message.answer(f"Вы должны переслать сообщение или написать id ({settings[0]['prefix']}id) человека.")
			else: return False

		msg = message.reply_to_message['from'] 
		member = await utils.getUser(chatdata['users'], msg.id)
		if(len(member) == 0): 
			if(not settings['serror']): return await message.answer("Данного пользователя нет в этом чате.")
			else: return False

	else:
		member = await utils.getUser(chatdata['users'], regexp_command.group(2))
		if(len(member) == 0): 
			if(not settings['serror']): return await message.answer("Данного пользователя нет в этом чате.") 
			else: return False

		msg = { "id": regexp_command.group(2), "first_name": member['fname'], "last_name": member['lname'] } 

	if(member['id'] == message.from_user.id):
		if(not settings['serror']): return await message.answer("Для того чтобы кикнуть самого себя пропишите \"самокик\".") 
		else: return False
	elif(member['rank'] == rangs.CREATOR):
		if(not settings['serror']): return await message.answer("Вы не можете кикнуть создателя чата.") 
		else: return False
	elif(member['rank'] >= user['rank']):
		if(not settings['serror']): return await message.answer("Данный пользователь выше или такого же ранга как Вы.") 
		else: return False

	await message.answer(text = f"Пользователь [{await utils.getName(msg)}](tg://user?id={msg['id']}) теперь может зайти по ссылке.", parse_mode='Markdown', disable_notification = True)
	await bot.unban_chat_member(message.chat.id, msg['id'])
