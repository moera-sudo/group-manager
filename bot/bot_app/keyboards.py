from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, WebAppData

from bot.config import config

startboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Открыть приложение', web_app=WebAppInfo(url=f'{config.API}/headman/account_main/1/posts'))
            ]
        ]
    )