from aiogram.utils.markdown import pre
from connector import dp, bot, db, data
from aiogram.types import ChatType
from config import commands, stng
from datetime import datetime
from aiogram import types
import time
import utils

# Команда для просмотра забаненых пользователей #
@dp.message_handler(gcm=(['^banlist$'], commands.banlist, True), chat_type=ChatType.SUPERGROUP)
async def banlist(message: types.Message, regexp_command):

	chatdata = data[message.chat.id*-1]

	if(len(chatdata['banned']) == 0):
		if(not chatdata['settings']['serror']): return await message.answer("Забаненых в чате нет.")
		else: return False

	msg = "Список забаненых пользователей:\n"
	c = 0
	for i in chatdata['banned']:
		user = await utils.getUser(chatdata['users'], i['id'])
		c += 1
		if(i['banto'] == 1):
			banto = "навсегда"
		elif(time.time() > i['banto']):
			await db.unban(message.chat.id, i['id'])
			await bot.unban_chat_member(message.chat.id, i['id'])
			banto = "уже разблокирован"
		else:
			banto = f"до {datetime.fromtimestamp(int(i['banto']))}"
		
		reason = '.'
		if(i['reason']):
			reason = f". Причина:{i['reason']}"
		
		id = pre(i['id'])
		msg += f"{c}. Пользователь: [{await utils.getNameDB(user)}](tg://user?id={i['id']}). ID: {id}\nЗаблокирован: {banto}{reason}\n"
	
	return await message.answer(msg, parse_mode='Markdown', disable_notification = True)