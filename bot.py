# Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
#updater = Updater(token='757939309:AAE3QMqbT8oeyZ44es-l6eSzxpy1toCf_Bk') # Токен API к Telegram        # Сам бот

#dispatcher = updater.dispatcher

from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

import sys
sys.path.append('../')
import threading
import time, pickle
import MySQLdb

from libs.player import *
from work_materials.class_filters import *
from work_materials.fraction_filters import *
from work_materials.other_initiate_filters import *

from bin.starting_player import *
from bin.save_load_user_data import *

import work_materials.globals


work_materials.globals.processing = 1

players = {}

def get_player(id):
    player = players.get(id)
    if player is not None:
        return player
    request = "SELECT "

def text_message(bot, update, user_data):
    pass



dispatcher.add_handler(CommandHandler("start", start, pass_user_data=True))

dispatcher.add_handler(MessageHandler(filter_classes, class_select, pass_user_data=True))

dispatcher.add_handler(MessageHandler(filter_fractions, fraction_select, pass_user_data=True))

dispatcher.add_handler(MessageHandler(filter_sex_select, sex_select, pass_user_data=True))

dispatcher.add_handler(MessageHandler(filter_nickname_select, nickname_select, pass_user_data=True))

dispatcher.add_handler(MessageHandler(Filters.text, text_message, pass_user_data=True))


loadData()
#print(dispatcher.user_data)
threading.Thread(target=saveData).start()
updater.start_polling(clean=True)


# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
work_materials.globals.processing = 0
# Разрываем подключение к базе данных
conn.close()