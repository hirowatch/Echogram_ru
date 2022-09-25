from handlers import bot, dp
from aiogram.utils import executor
from datetime import datetime
from data.functions.models import Admins

class Notification():
	def __init__(self):
		self.admins = Admins.select(Admins.id)
		self.date = datetime.now().date()
	async def on(self, dp):
		for admin in self.admins:
			try:
				await bot.send_message(admin, f"{self.date}: Бот запущен")
			except: pass
	async def off(self, dp):
		for admin in self.admins:
			try:
				await bot.send_message(admin, f"{self.date}: Бот остановлен")
			except: pass

if __name__ == "__main__":
	strike = Notification()
	executor.start_polling(dp, on_startup=strike.on, on_shutdown=strike.off, skip_updates=True)