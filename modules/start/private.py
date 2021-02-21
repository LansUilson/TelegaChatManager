from aiogram.types import ChatType
from config import commands 
from connector import dp, bot
from aiogram import types
import utils

# Команда старт для привата #
@dp.message_handler(gcm=(['^start$'], commands.stats), chat_type=ChatType.PRIVATE)
async def start(message: types.Message):
	keyboard_markup = types.InlineKeyboardMarkup()
	keyboard_markup.add(
		types.InlineKeyboardButton('Как это сделать?', callback_data='howToAdd'),
	)
	await message.answer("🔸Привет👋\n🔸Меня зовут Чат-Менеджер!\n🔸По названию ты наверное понял, что я бот для модерирования чата.\n🔸Так вот, чтобы я смог модерировать чат, ты должен меня туда добавить и выдать права администратора.", reply_markup=keyboard_markup)
	
@dp.callback_query_handler(text='howToAdd', chat_type=ChatType.PRIVATE)
async def howToAddToChat(query: types.CallbackQuery):
	await bot.edit_message_reply_markup(query.from_user.id, query.message.message_id, [])
	await bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id, text="🔸Не знаешь как?\n🔸Это очень просто!\n🔸Ты должен быть администратором или создателем чата.\n🔸Тебе нужно зайти в настройки группы, нажать 'Добавить участника' и выбрать Чат-Менеджера!")
 