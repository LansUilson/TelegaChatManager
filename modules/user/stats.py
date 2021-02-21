from aiogram.types import ChatType
from connector import dp, data
from config import commands
from aiogram import types
import asyncio
import utils

# Send user information #
@dp.message_handler(gcm=(['^stats$'], commands.stats), chat_type=ChatType.SUPERGROUP)
async def stats(message: types.Message):
	
	user = await utils.getUser(data[int(str(message.chat.id).replace('-', ''))]['users'], message.from_user.id)

	if(user['rank'] == 1): rank = "Пользователь"
	elif(user['rank'] == 2): rank = "Администратор"
	elif(user['rank'] == 3): rank = "Создатель"

	await message.answer(text = f"""
Статистика [{await utils.getName(message.from_user)}](tg://user?id={message.from_user.id}):
  Ранг: {rank}
  Уровень: {user['level']}
  Опыт: {user['exp']}/{user['needexp']}
  Сообщений: {user['mess']}
  Сообщений не подряд: {user['messncons']}
""", parse_mode='Markdown', disable_notification = True)
