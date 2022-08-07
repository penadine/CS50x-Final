from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

""" Initialisation of bot. """
storage = MemoryStorage()
bot = Bot('5468570358:AAHNBc26_nNEfdWCKNCKoNELJhfzir0W2F8')
dp = Dispatcher(bot, storage=storage)