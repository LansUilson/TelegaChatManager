from aiogram.dispatcher.filters import BoundFilter
from connector import dp, db, bot, data
from difflib import get_close_matches
from config import rangs, stng, times
from aiogram import types
import re

# Ниже приведены фильтры, созданные модулем aiogram. #

class IsCommand(BoundFilter):
	"""
	Фильтр для проверки сообщения на команду. 
	
	Проверяет наличие префикса чата в сообщении.
	"""

	key = 'not_command'

	def __init__(self, not_command):
		self.not_command = not_command

	async def check(self, message: types.Message):
		if(not message.text.startswith(data[message.chat.id*-1]['settings']['prefix'])):
			return True
		return False

class getCorrectMess(BoundFilter):

	"""
	Код взят из официального репозитория aiogram
	(https://github.com/aiogram/aiogram/blob/dev-2.x/aiogram/dispatcher/filters/builtin.py (417-435 строки)),

	Этот фильтр улучшен специально под этого бота. 
	gcm - ключ фильтра.
	"""

	key = 'gcm'

	def __init__(self, gcm):
		self.gcm = [re.compile(command, flags=re.IGNORECASE | re.MULTILINE) for command in gcm[0]]
		self.pattern = gcm[1]
		self.checkadmin = None
		if len(gcm) == 3: self.checkadmin = gcm[2]

	async def check(self, message: types.Message):
		cmd = message.text.split()[0].lower()
		sim = get_close_matches(cmd, self.pattern)

		if len(sim) == 0: return False

		for i in range(0, len(sim)):

			if len(sim[i]) == len(cmd) or len(sim[i])+1 == len(cmd):

				chatdata = data[message.chat.id*-1] # (*-1) - это делается для того, чтобы убрать знак минуса, т.к БД не примимает в схему минусовые значения

				if not checkExist(message.from_user.id, chatdata): await createDefaultUser(message) 
				
				if self.checkadmin:
					if not await isAdmin(message, chatdata['users']): return False 

				if sim[i] in stng.cmds: 
					if chatdata['ofdcmds'][sim[i]]: return False

				if not message.text.startswith(chatdata['settings']['prefix']): return False 

				if chatdata['settings']['autoreplace']: message.text = message.text.replace(message.text.split()[0], self.pattern[0])
				else: message.text = message.text.replace(message.text.split()[0], message.text.split()[0][1:])

				command = message.text.split()[0]

				command, _, mention = command.partition('@')

				if mention and mention != (await message.bot.me).username: return False

				for command in self.gcm:

					search = command.search(message.text)

					if search:
						''' Это на всякий случай, 
						   лучше использовать глобальную переменную data, 
						   если пользоваться тем, что снизу, 
						   то придётся всё сохранять'''
						return {'regexp_command': search, "users": chatdata['users'], "chat": chatdata['chat'], "settings": chatdata['settings'], "ofdcmds": chatdata['ofdcmds'], "banned": chatdata['banned']}
				return False
			return False

dp.filters_factory.bind(IsCommand)
dp.filters_factory.bind(getCorrectMess)

"""
Ниже переведены вспомогательные функции
"""

async def getName(userdata):
	"""
	Проверяет пользователя на фамилию
	И возвращает никнейм с именем или с именем и фамилией. 
	"""

	if(str(userdata['last_name']) == "None"): 
		return f"{userdata['first_name']}"

	elif(str(userdata['last_name']) != "None"): 
		return f"{userdata['first_name']} {userdata['last_name']}"

async def isAdmin(message, fdb, type=0):
	"""
	Проверка на администратора беседы.
	Проверка происходит за счёт БД и самого телеграма.
	"""

	from_db = await getUser(fdb, message.from_user.id)
	member = await bot.get_chat_member(message.chat.id, message.from_user.id) 

	if(from_db['rank'] > rangs.USER or member.is_chat_admin()):
		return True
	return False

async def getUser(data, id, number=False):
	''' Код украден со stackoverflow.com :) '''

	def show_indices(obj, indices):
	    for k, v in obj.items() if isinstance(obj, dict) else enumerate(obj):
	        if isinstance(v, (dict, list)):
	            yield from show_indices(v, indices + [k])
	        else:
	            yield indices + [k], v
	
	for keys, v in show_indices(data, [] ):
	   if(str(v) == str(id)):
	    	if(number):
	    		return keys[0]
	    	return data[keys[0]]

async def convert_time(value, date):
	''' Конвертация времени для команды ban '''
	value = int(value)
	if(date in times.min):
		return 60*value, f" на {value} минут(-ы)"
	elif(date in times.hr):
		return 3600*value, f" на {value} часа(-ов)"
	elif(date in times.day):
		return 86400*value, f" на {value} дня(-ей)"
	elif(date in times.week):
		return 604800*value, f" на {value} недели(-ль)"
	elif(date in times.month):
		return 2678400*value, f" на {value} месяц(-ев)"
	elif(date in times.year):
		if(value <= 4):
			return 31536000*value, f" на {value} год(-а)"
		return 31536000*value, f" на {value} лет"
	else:
		return None

def checkExist(user_id, chatdata):
	''' Проверка на существование пользователя '''
	for i in chatdata['users']:
		if(i['id'] == user_id):
			return True
	return False

async def createDefaultUser(message):
	''' Внесение пользователя в БД '''
	member = await bot.get_chat_member(message.chat.id, message.from_user.id)
	if(member.status == "creator"):
		rank = rangs.CREATOR
	elif(member.status == "admin"):
		rank = rangs.ADMIN
	else:
		rank = rangs.USER 
	return await db.create_user(chat_id=message.chat.id, id=message.from_user.id, rank=rank, first_name=message.from_user.first_name, last_name=message.from_user.last_name)
