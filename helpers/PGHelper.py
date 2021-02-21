from config import DATADB, stng
from connector import logging
import threading
import asyncio
import pg8000
import time
import json 

# Обход блокировки aiogram'а #'
class RunThread(threading.Thread):
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        super().__init__()

    def run(self):
        self.result = asyncio.run(self.func(*self.args, **self.kwargs))

def run_async(func, *args, **kwargs):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    if loop and loop.is_running():
        thread = RunThread(func, args, kwargs)
        thread.start()
        thread.join()
        return thread.result
    else:
        return asyncio.run(func(*args, **kwargs))


class Helper:
	# Подключение к БД #
	def __init__(self, info):
		self.conn = pg8000.connect(**DATADB)

		global data

		schemas = self.conn.run("""SELECT '' || schema_name || '' AS query 
														FROM information_schema.schemata
														WHERE schema_name IN
														(
														    SELECT schema_name 
														    FROM information_schema.schemata
														    WHERE schema_name NOT LIKE 'pg_%' AND schema_name != 'information_schema'
														);"""
		)

		query = ""
		data = {}
		for i in schemas:
			ais = self.conn.run(f"SELECT row_to_json (rows) FROM (SELECT * FROM {i[0]}.chat) rows; SELECT row_to_json (rows) FROM (SELECT * FROM {i[0]}.settings) rows; SELECT row_to_json (rows) FROM (SELECT * FROM {i[0]}.users) rows; SELECT row_to_json (rows) FROM (SELECT * FROM {i[0]}.ofdcmds) rows; SELECT row_to_json (rows) FROM (SELECT * FROM {i[0]}.banned) rows;")

			data.update({
				ais[0][0]['id']: {
					"users": [],
					"chat": {}, 
					"settings": {},
					"ofdcmds": {}, 
					"banned": []
				} 
			})

			for u in ais:
				if("first_name" in str(u)): data[ais[0][0]['id']]['users'].append(u[0])
				if("lastsender" in str(u)): data[ais[0][0]['id']]['chat'].update(u[0])
				if("serror" in str(u)): data[ais[0][0]['id']]['settings'].update(u[0])
				if("unban" in str(u)): data[ais[0][0]['id']]['ofdcmds'].update(u[0])
				if("banto" in str(u)): data[ais[0][0]['id']]['banned'].append(u[0])

		Helper.updateDB(self)

	# Создание пустого шаблона чата #
	async def create_chat_default(self, chat_id):

		chat_id=chat_id*-1 

		query = f"""CREATE TABLE IF NOT EXISTS sc{chat_id}.ofdcmds("""
		cursor = self.conn.cursor()

		for i in range(0, len(stng.cmds)):
			if(i == 0):
				query+=f"""	
	{stng.cmds[i]}	boolean	DEFAULT	false,
"""
			elif(not i == len(stng.cmds)-1):
				query+=f"""	{stng.cmds[i]}	boolean	DEFAULT	false,
"""
			elif(i == len(stng.cmds)-1):
				query+=f"""	{stng.cmds[i]}	boolean	DEFAULT	false
);"""

		self.conn.run(f"""CREATE SCHEMA IF NOT EXISTS sc{chat_id};
			CREATE TABLE IF NOT EXISTS sc{chat_id}.users(
				id				numeric				UNIQUE NOT NULL, 
				first_name		varchar, 
				last_name		varchar, 
				mess			numeric		DEFAULT 0,
				messncons	numeric	DEFAULT 0,
				rank			int  			 	DEFAULT 1, 
				level			int	 		 		DEFAULT 1,
				exp	 			double precision	DEFAULT 0.0, 
				needexp			int			  		DEFAULT 55
			);
			CREATE TABLE IF NOT EXISTS sc{chat_id}.chat(
				id					numeric		UNIQUE NOT NULL,
				name			varchar,
				lastsender	numeric				DEFAULT 0,
				level		int	 		 		DEFAULT 1,
				exp	 		double precision	DEFAULT 0.1, 
				needexp		int			  		DEFAULT 200, 
				mess			numeric			DEFAULT 0, 
				messncons	numeric		DEFAULT 0
			);
			INSERT INTO sc{chat_id}.chat (name, id) SELECT 'Да', {chat_id} WHERE NOT EXISTS ( SELECT * FROM sc{chat_id}.chat );
			CREATE TABLE IF NOT EXISTS sc{chat_id}.settings(
				serror			boolean				DEFAULT	false,
				autoReplace	boolean		DEFAULT false, 
				welcome	varchar				DEFAULT 'Добро пожаловать в чат!', 
				prefix		varchar				DEFAULT	'/'
			);
			CREATE TABLE IF NOT EXISTS sc{chat_id}.banned(
				id	    	numeric		UNIQUE NOT NULL,
				banto	 numeric		DEFAULT	0, 
				reason   varchar		 DEFAULT	NULL
			);
			INSERT INTO sc{chat_id}.settings (serror) SELECT false WHERE NOT EXISTS ( SELECT * FROM sc{chat_id}.settings );
			{query}
			INSERT INTO sc{chat_id}.ofdcmds (id) SELECT false WHERE NOT EXISTS ( SELECT * FROM sc{chat_id}.ofdcmds );"""
		)
		self.conn.commit()
		
		ais = self.conn.run(f"SELECT row_to_json (rows) FROM (SELECT * FROM sc{chat_id}.chat) rows; SELECT row_to_json (rows) FROM (SELECT * FROM sc{chat_id}.settings) rows; SELECT row_to_json (rows) FROM (SELECT * FROM sc{chat_id}.users) rows; SELECT row_to_json (rows) FROM (SELECT * FROM sc{chat_id}.ofdcmds) rows; SELECT row_to_json (rows) FROM (SELECT * FROM sc{chat_id}.banned) rows;")

		data.update({
			ais[0][0]['id']: {
				"users": [],
				"chat": {}, 
				"settings": {},
				"ofdcmds": {}, 
				"banned": []
			} 
		})

		for u in ais:
			if("first_name" in str(u)): data[ais[0][0]['id']]['users'].append(u[0])
			if("lastsender" in str(u)): data[ais[0][0]['id']]['chat'].update(u[0])
			if("serror" in str(u)): data[ais[0][0]['id']]['settings'].update(u[0])
			if("unban" in str(u)): data[ais[0][0]['id']]['ofdcmds'].update(u[0])
			if("banto" in str(u)): data[ais[0][0]['id']]['banned'].append(u[0])

	# Создание юзера в таблице #
	async def create_user(self, chat_id, id, first_name, last_name, rank=1):

		chat_id=chat_id*-1
		data[chat_id]['users'].append({'id': id, 'first_name': first_name, 'last_name': last_name, 'mess': 0, 'messncons': 0, 'rank': rank, 'level': 1, 'exp': 0.0, 'needexp': 55}) 

		self.conn.run(f"""
			INSERT INTO 
				 sc{chat_id}.users (id, first_name, last_name, rank) 
			VALUES
				 ({id}, '{first_name}', '{last_name}', {rank});"""
		)
		self.conn.commit()
	
	# Внесение пользователя в таблицу забаненых #
	async def ban(self, chat_id, id, banto, reason="NULL"):

		chat_id=chat_id*-1
		data[chat_id]['banned'].append({'id': int(id), 'banto': banto, 'reason': reason})

		self.conn.run(f"""
			INSERT INTO 
				 sc{chat_id}.banned (id, banto, reason) 
			VALUES
				 ({id}, {banto}, '{reason}');"""
		)
		self.conn.commit()

	# Удаление пользователя из таблицы забаненных #
	async def unban(self, chat_id, id):

		chat_id=chat_id*-1 

		for i in range(0, len(data[chat_id]['banned'])):
			if(data[chat_id]['banned'][i]['id'] == int(id)):
				del data[chat_id]['banned'][i]

		self.conn.run(f"""
			DELETE FROM
				 sc{chat_id}.banned
			WHERE
				 id = {id};"""
		)
		self.conn.commit() 

	# Обновление БД через какое-то время #
	def updateDB(self):
		logging.info("DATABASE UPDATED")
		threading.Timer(600.0, Helper.updateDB, args=[self]).start()

		query = ''
		for i in data:
			for u in data[i]['users']:
				query += f"""
				UPDATE sc{i}.users 
				SET
					(id, first_name, last_name, mess, messncons, rank, level, exp, needexp) = 
					({u['id']}, '{u['first_name']}', '{u['last_name']}', {u['mess']}, {u['messncons']}, {u['rank']}, {u['level']}, {u['exp']}, {u['needexp']}) 
				WHERE 
					id = {u['id']};"""

			for b in data[i]['banned']:
				query += f"""
				UPDATE sc{i}.banned 
				SET
					(id, banto) = 
					({b['id']}, {b['banto']}) 
				WHERE 
					id = {b['id']};"""

			query += f"""
			UPDATE sc{i}.chat 
			SET 
				(lastsender, level, exp, needexp) = 
				({data[i]['chat']['lastsender']}, {data[i]['chat']['level']}, {data[i]['chat']['exp']}, {data[i]['chat']['needexp']});
			UPDATE sc{i}.settings 
			SET 
				(serror, autoreplace, prefix, welcome) = 
				({data[i]['settings']['serror']}, {data[i]['settings']['autoreplace']}, '{data[i]['settings']['prefix']}',  '{data[i]['settings']['welcome']}');
			UPDATE sc{i}.ofdcmds 
			SET 
				(id, prefix, kick, ban, unban, banlist, stats, welcome) = 
				({data[i]['ofdcmds']['id']}, {data[i]['ofdcmds']['prefix']}, {data[i]['ofdcmds']['kick']}, {data[i]['ofdcmds']['ban']}, {data[i]['ofdcmds']['unban']}, {data[i]['ofdcmds']['banlist']}, {data[i]['ofdcmds']['stats']}, '{data[i]['ofdcmds']['welcome']}')"""
		
		if(len(query) == 0):
			return False

		self.conn.run(query)
		return self.conn.commit()

#	async def close(self):
#		self.connection.close()
#		return True
