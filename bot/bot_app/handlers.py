from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from .keyboards import startboard


#Обработчик команды Start
async def start_command_handler(message: Message):
    # print(API)
    await message.answer("Добро пожаловать, начните участвовать в функционировании вашей группы уже сейчас с помощью нашего мини-приложения", reply_markup=startboard)


#--Экспортируемый регистратор обработчиков
def register_handlers(dp: Dispatcher):
    dp.message.register(start_command_handler, CommandStart)