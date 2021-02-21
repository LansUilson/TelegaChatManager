from config import commands, admin, user, rangs
from aiogram.types import ChatType
from connector import dp, bot, data
from aiogram import types
import utils

# Изменение статуса пользователей #
@dp.message_handler(gcm=(['^setrang(?:( +(\d+)|) +([a-zA-Zа-яА-я]+))$'], commands.setrang, True), chat_type=ChatType.SUPERGROUP)
async def setrang(message: types.Message, regexp_command):

	if((await bot.get_chat_member(message.chat.id, message.from_user.id)).status == "creator"):
		chatdata = data[message.chat.id*-1]

		if(not regexp_command.group(1)):
			if(not "reply_to_message" in str(message)):
				if(not chatdata['settings']['serror']): return await message.answer(f"Вы должны переслать сообщение или написать id ({settings[0]['prefix']}id) человека.")
				else: return False
			
			msg = message.reply_to_message['from']
			member = await utils.getUser(chatdata['users'], msg.id)
			if(not member): 
				if(not chatdata['settings']['serror']): return await message.answer("Данного пользователя нет в этом чате.")
				else: return False
		else:
			member = await utils.getUser(chatdata['users'], regexp_command.group(1))
			if(not member): 
				if(not chatdata['settings']['serror']): return await message.answer("Данного пользователя нет в этом чате.") 
				else: return False
	
			msg = { "id": int(regexp_command.group(1)), "first_name": member['first_name'], "last_name": member['lastname'] } 
		
		if(msg['id'] == message.from_user.id): return await message.answer("Вы не можете изменить свои права, так как вы владелец чата.")

		if(regexp_command.group(3).lower() in admin):
			usern = await utils.getUser(chatdata['users'], msg['id'], True)
			chatdata['users'][usern]['rank'] = rangs.ADMIN
			return await message.answer(text = f"Теперь пользователь [{await utils.getName(msg)}](tg://user?id={msg['id']}) является администратором.", parse_mode='Markdown', disable_notification = True)
		elif(regexp_command.group(3).lower() in user):
			usern = await utils.getUser(chatdata['users'], msg['id'], True)
			chatdata['users'][usern]['rank'] = rangs.USER
			return await message.answer(text = f"Теперь пользователь [{await utils.getName(msg)}](tg://user?id={msg['id']}) является обычным пользователем.", parse_mode='Markdown', disable_notification = True)
		
		return await message.answer("Неизвестный ранг.")