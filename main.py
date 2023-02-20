from datetime import datetime
import os
import time

from aiogram import Bot, Dispatcher, executor, types
import requests

import parser
import config


bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()  # commands=['Кировский']
async def echo_kirov(message: types.Message):
    # await message.answer(message.text)
    # await message.reply(message.text)  # Ответ с цитатой пользователя
    # В этом варианте сообщение приходит пользователю, если он ранее писал боту, иначе ошибка
    await bot.send_message(message.chat.id, f"Ответ: НЕТ")

executor.start_polling(dp, skip_updates=True)
