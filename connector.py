"""
Initialization logging 
"""
from config import LOGGING_TYPE
import datetime
import asyncio
import logging
import time 

date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d') 
times = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

if(LOGGING_TYPE == "file"):
	logging.basicConfig(level=logging.DEBUG, filename=f'./logs/{date}.log', filemode='a', format=f'[{times}] [%(levelname)s] %(name)s: %(message)s') 
elif(LOGGING_TYPE == "console"):
	logging.basicConfig(level=logging.DEBUG, format=f'[{times}] [%(levelname)s] %(name)s: %(message)s') 

logging.info("The logging is initiated")

"""
Initialization DB
"""
from helpers.PGHelper import Helper
from config import DATADB
import asyncio

global db, data
db = Helper(DATADB)
from helpers.PGHelper import data

logging.info("The database is initialized")

"""
Connect to AIOGram
"""
from config import API_TOKEN
from aiogram import Bot, Dispatcher

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

logging.info("Connected to AIOGram")

"""
Loading modules
"""
from modulesLoad import load
load()

logging.info("The modules are loaded")
