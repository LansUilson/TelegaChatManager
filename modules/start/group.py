from aiogram.types import ChatType
from connector import dp, bot, db
from aiogram import types

@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS, chat_type=ChatType.SUPERGROUP)
async def ifAddToChat(message: types.ContentTypes):
	users = []
	for i in range(0, len(message.new_chat_members)):
		users.append(message.new_chat_members[i].id)

	if(1275160567 in users):
		keyboard_markup = types.InlineKeyboardMarkup()
		keyboard_markup.add(
			types.InlineKeyboardButton('Как это сделать?', callback_data='howToAddAdmin'),
		)

		await message.answer("🔸Привет👋\n🔸Меня зовут Чат-Менеджер!\n🔸Для того, чтобы я нормально работал мне нужны права администратора.\n🔸Не бойтесь, вашей прекрасной беседе я ничего не сделаю!", reply_markup=keyboard_markup)
		await db.create_chat_default(message.chat.id)
	else:
		welcome = await db.get_settings(message.chat.id) 
		await message.answer(welcome[0][0]["welcome"])

@dp.callback_query_handler(text='howToAddAdmin', chat_type=ChatType.SUPERGROUP)
async def howToAddAdmin(query: types.CallbackQuery):
	await bot.edit_message_reply_markup(query.message.chat.id, query.message.message_id, [])
	await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text="🔸Для выдачи прав администратора нужно владельцу или администратору надо нажать на редактирование чата, потом на участники, выбрать Чат-Менеджера и нажать на 'Сделать администратором'.\n🔸Это нужно для того, чтобы бот исключительно по вашему запросу и запросу администраторов кикал человека из беседы.\n🔸Приятного пользования!")
