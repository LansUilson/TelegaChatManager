from config import commands, stng, rangs
from aiogram.types import ChatType
from connector import dp, bot, data
from aiogram import types
import utils

# Команда для просмотра топов #
@dp.message_handler(gcm=(['^top$'], commands.top), chat_type=ChatType.SUPERGROUP)
async def top(message: types.Message, regexp_command):

	keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
	keyboard_markup.add(
		types.InlineKeyboardButton('Топ пользователей', callback_data='usersTop'),
		types.InlineKeyboardButton('Топ чатов', callback_data='chatsTop'),
	)

	await message.answer("Выберите, по какой группе нужно составить топ.", reply_markup=keyboard_markup)

@dp.callback_query_handler(text='usersTop', chat_type=ChatType.SUPERGROUP)
async def usersTop(query: types.CallbackQuery):
	keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
	keyboard_markup.add(
		types.InlineKeyboardButton('Топ по сообщениям', callback_data='usersMessTop'),
		types.InlineKeyboardButton('Топ по уровню', callback_data='usersLevelTop'),
	)

	await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=keyboard_markup, text="Выберите, по каким параметрам нужно составить топ пользователей.")

@dp.callback_query_handler(text=['usersMessTop', 'usersLevelTop'], chat_type=ChatType.SUPERGROUP)
async def usersMaLTop(query: types.CallbackQuery):
	chatdata = data[query.message.chat.id*-1]
	users = chatdata['users']
	
	if(query.data == 'usersMessTop'):
		sort = sorted(users, key=lambda x : x['mess'], reverse=True)

		mess = "Топ пользователей по сообщениям в Вашем чате:\n" 

		count = 0
		for i in sort:
			count += 1
			mess += f"{count}. Пользователь: [{await utils.getName(i)}](tg://user?id={i['id']}).\nСообщений: {i['mess']}.\n"

	elif(query.data == 'usersLevelTop'):
		sort = sorted(users, key=lambda x : x['level'], reverse=True)

		mess = "Топ пользователей по уровню в Вашем чате:\n" 

		count = 0
		for i in sort:
			count += 1
			mess += f"{count}. Пользователь: [{await utils.getName(i)}](tg://user?id={i['id']}).\nУровень: {i['level']}.\n"

	await bot.edit_message_reply_markup(query.message.chat.id, query.message.message_id, [])
	await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=mess, parse_mode='Markdown')

@dp.callback_query_handler(text='chatsTop', chat_type=ChatType.SUPERGROUP)
async def usersTop(query: types.CallbackQuery):
	keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
	keyboard_markup.add(
		types.InlineKeyboardButton('Топ по сообщениям', callback_data='chatsMessTop'),
		types.InlineKeyboardButton('Топ по уровню', callback_data='chatsLevelTop'),
	)

	await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=keyboard_markup, text="Выберите, по каким параметрам нужно составить топ чатов.")

@dp.callback_query_handler(text=['chatsMessTop', 'chatsLevelTop'], chat_type=ChatType.SUPERGROUP)
async def chatsMaLTop(query: types.CallbackQuery):
	
	chats = []
	for i in data:
		chats.append(data[i]['chat'])

	if(query.data == 'chatsMessTop'):
		sort = sorted(chats, key=lambda x : x['mess'], reverse=True)

		mess = "Топ чатов по сообщениям:\n" 

		count = 0
		for i in sort:
			count += 1
			mess += f"{count}. Чат: {i['name']}\nСообщений: {i['mess']}.\n"

	elif(query.data == 'chatsLevelTop'):
		sort = sorted(chats, key=lambda x : x['level'], reverse=True)

		mess = "Топ чатов по уровню:\n" 

		count = 0
		for i in sort:
			count += 1
			mess += f"{count}. Чат: {i['name']}.\nУровень: {i['level']}.\n"

	await bot.edit_message_reply_markup(query.message.chat.id, query.message.message_id, [])
	await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=mess, parse_mode='Markdown')

