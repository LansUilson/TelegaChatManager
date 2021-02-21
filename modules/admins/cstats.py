from aiogram.types import ChatType
from connector import dp, data
from config import commands
from aiogram import types
import utils

# Команда для просмотра статистики чата #
@dp.message_handler(gcm=(['^chatstats$'], commands.chatstats, True), chat_type=ChatType.SUPERGROUP)
async def cstats(message: types.Message):

	chat = data[message.chat.id*-1]['chat']

	await message.answer(text = f"""
Статистика вашего чата ({chat['name']}):
  Уровень: {chat['level']}
  Опыт: {chat['exp']}/{chat['needexp']}
  Сообщений: {chat['mess']}
  Сообщений не подряд: {chat['messncons']}
""", parse_mode='Markdown', disable_notification = True)
