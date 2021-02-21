from connector import dp, logging
from aiogram import executor
import modules

if __name__ == "__main__":
	logging.info("Started") 
	executor.start_polling(dp)
