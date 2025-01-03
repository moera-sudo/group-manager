import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


from .config import config
from .bot_app.handlers import register_handlers


dp = Dispatcher()

async def main() -> None:
    try:
        
        bot = Bot(token=config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        register_handlers(dp)
        await dp.start_polling(bot)

    except Exception as e:
        logging.basicConfig(level=logging.INFO)
        print("Ошибка работы бота", str(e))

if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot dropped')