# Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
updater = Updater(token='757939309:AAE3QMqbT8oeyZ44es-l6eSzxpy1toCf_Bk') # Токен API к Telegram        # Сам бот

dispatcher = updater.dispatcher

from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

import sys
sys.path.append('../')

from libs.player import *


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Выберите имя")
    return
    #player = Player(update.message.chat_id, update.message.user_from.username, update.message.user_from.username, )



dispatcher.add_handler(CommandHandler("start", start))


updater.start_polling(clean=True)

# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
# Разрываем подключение.
#conn.close()