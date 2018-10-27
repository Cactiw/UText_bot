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

from libs import player, mage, warrior
from work_materials.class_filters import *
from work_materials.fraction_filters import *
from work_materials.other_initiate_filters import *

from bin.starting_player import *
from bin.save_load_user_data import *

import work_materials.globals


work_materials.globals.processing = 1

players = {}

def get_player(id):
    pass

def text_message(bot, update, user_data):
    pass

def choose_skill(bot, update):
    id = update.message.from_user.id
    player = get_player(id)
    if player is None:
        return
    free_skill = player.free_skill_points
    if free_skill == 0:
        bot.sendmessage(chat_id = update.message.chat_id, text = "У вас нет очков навыков")
        return

    player.status = "Lvl_up_skill"
    button_list = [
        KeyboardButton("1"),
        KeyboardButton("2"),
        KeyboardButton("3"),
        KeyboardButton("4"),
        KeyboardButton("5"),
        KeyboardButton("Назад")
    ]
    buttons = ReplyKeyboardMarkup(build_menu(button_list, n_cols=2), resize_keyboard=True, one_time_keyboard = True)

    if free_skill == 1:
        bot.sendmessage(chat_id=update.message.chat_id,
                        text = "Вы можете улучшить <b>1</b> навык\nВыберите навык, который хотите улучшить\n"
                               "Первый навык - {0}-го уровня\nВторой навык - {1}-го уровня\n"
                               "Третий навык - {2}-го уровня\nЧетвертый навык - {3}-го уровня\n"
                               "Пятый навык - {4}-го уровня".format(player.first_skill_lvl, player.second_skill_lvl,
                                                                    player.third_skill_lvl, player.fourth_skill_lvl,
                                                                    player.fifth),
                        parse_mode = 'HTML', reply_markup = buttons)

    elif free_skill >= 2 and free_skill <= 4:
        bot.sendmessage(chat_id=update.message.chat_id,
                        text="Вы можете улучшить <b>{0}</b> навыкa\nВыберите навык, который хотите улучшить\n"
                             "Первый навык - {1}-го уровня\nВторой навык - {2}-го уровня\n"
                             "Третий навык - {3}-го уровня\nЧетвертый навык - {4}-го уровня\n"
                             "Пятый навык - {5}-го уровня".format(free_skill, player.first_skill_lvl,
                                                                  player.second_skill_lvl, player.third_skill_lvl,
                                                                  player.fourth_skill_lvl, player.fifth),
                        parse_mode='HTML', reply_markup = buttons)
    elif free_skill >= 5:
        bot.sendmessage(chat_id=update.message.chat_id,
                        text="Вы можете улучшить <b>{0}</b> навыков\nВыберите навык, который хотите улучшить\n"
                             "Первый навык - {1}-го уровня\nВторой навык - {2}-го уровня\n"
                             "Третий навык - {3}-го уровня\nЧетвертый навык - {4}-го уровня\n"
                             "Пятый навык - {5}-го уровня".format(free_skill, player.first_skill_lvl,
                                                                  player.second_skill_lvl, player.third_skill_lvl,
                                                                  player.fourth_skill_lvl, player.fifth),
                        parse_mode='HTML', reply_markup = buttons)


def lvl_up_skill():
    pass #TODO

dispatcher.add_handler(CommandHandler("start", start, pass_user_data = True))

dispatcher.add_handler(MessageHandler(filter_classes, class_select, pass_user_data = True))

dispatcher.add_handler(MessageHandler(filter_fractions, fraction_select, pass_user_data = True))

dispatcher.add_handler(MessageHandler(filter_sex_select, sex_select, pass_user_data = True))

dispatcher.add_handler(MessageHandler(filter_nickname_select, nickname_select, pass_user_data = True))

dispatcher.add_handler(CommandHandler("lvl_up", choose_skill, pass_user_data = False))
dispatcher.add_handler(MessageHandler(filter_lvl_up_skill, lvl_up_skill, pass_user_data = False))

#-------------------
dispatcher.add_handler(MessageHandler(Filters.text, text_message, pass_user_data = True))



loadData()
#print(dispatcher.user_data)
threading.Thread(target=saveData).start()
updater.start_polling(clean=True)

# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
work_materials.globals.processing = 0
# Разрываем подключение к базе данных
conn.close()