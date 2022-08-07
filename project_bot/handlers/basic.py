from buttons.buttons import main_menu, intomain_menu
from aiogram import types, Dispatcher
from configuration.create_bot import bot

""" /start, /Main_menu"""
async def start(message: types.Message):
    await message.answer(f'Welcome to my telegram bot!\nPlease, pick the menu button.', reply_markup=main_menu)

""" /Help """
async def help(message: types.Message):
    await message.answer(f'For the help watch this wideo:\n\n[TUTORIAL](https://youtu.be/bgsPYW_0yYc)', parse_mode='markdown', disable_web_page_preview=True,  reply_markup=intomain_menu)

""" [inline URL](https://youtu.be/bgsPYW_0yYc) """

def register_handlers_basic(dp : Dispatcher):
    dp.register_message_handler(start, commands=['start', 'Main_menu'])
    dp.register_message_handler(help, commands=['Help'])