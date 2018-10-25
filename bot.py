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

from work_materials.globals import *



#Подключаем базу данных, выставляем кодировку
print("Enter password for database:")
passwd = input()
print(passwd)
conn = MySQLdb.connect('localhost', 'UText_bot', passwd, 'UText_bot')

cursor = conn.cursor()
conn.set_character_set('utf8')
#conn.set_character_set('utf8mb4')
#cursor.execute('SET NAMES utf8mb4;')
#cursor.execute('SET CHARACTER SET utf8mb4;')
#cursor.execute('SET character_set_connection=utf8mb4;')
print("Connection successful, starting bot")
processing = 1

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def start(bot, update, user_data):
    user_data.update(type = 1)
    request = "SELECT * FROM PLAYERS WHERE id = '{0}'".format(update.message.from_user.id)
    cursor.execute(request)
    row = cursor.fetchone()
    if row is not None:
        bot.send_message(chat_id=update.message.chat_id, text="Вы уже в игре!")
        return

    button_list = [
        KeyboardButton("Люди"),
        KeyboardButton("Орки"),
        KeyboardButton("Эльфы")
    ]
    reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=3))
    bot.send_message(chat_id=update.message.chat_id, text="Выберите фракцию, за которую вы будете сражаться!", reply_markup = reply_markup)
    return

def fraction_select(bot, update, user_data):
    type = user_data.get('type')
    if type is 1:   # Выбор фракции
        user_data.update({'fraction': update.message.text, 'type': 2})

        button_list = [
            KeyboardButton("Люди"),
            KeyboardButton("Орки"),
            KeyboardButton("Эльфы")
        ]
        reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=3))

        bot.send_message(chat_id=update.message.chat_id, text="Вы выбрали фракцию <b>{0}</b>\n"
                                                              "Теперь необходимо выбрать расу!".format(
            user_data.get('fraction')), parse_mode='HTML', reply_markup=reply_markup)
        return
    elif type is 2:    # Выбор расы
        race_select(bot, update, user_data)

def race_select(bot, update, user_data):
    user_data.update({'race': update.message.text, 'type': 3})

    button_list = [
        KeyboardButton("Воин"),
        KeyboardButton("Маг"),
        KeyboardButton("Лучник"),
        KeyboardButton("Клирик"),
    ]
    reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=2))

    bot.send_message(chat_id=update.message.chat_id, text="Вы выбрали расу <b>{0}</b>\n"
                                                          "Теперь необходимо выбрать класс!".format(
        user_data.get('race')), parse_mode='HTML', reply_markup=reply_markup)
    return

def class_select(bot, update, user_data):
    user_data.update({'class' : update.message.text, 'type' : 4})
    button_list = [
        KeyboardButton("Мужской"),
        KeyboardButton("Женский"),
    ]
    reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=1))
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Отлично, вы выбрали класс <b>{0}</b>\n"
             "Выберите пол:".format(user_data.get('class')),
        parse_mode = 'HTML', reply_markup = reply_markup)
    return

def sex_select(bot, update, user_data):
    user_data.update(sex=update.message.text, type=5)
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Отлично, осталось всего лишь выбрать имя, "
             "под которым вас будут знать другие игроки!".format(user_data.get('class')),
        parse_mode='HTML', reply_markup=ReplyKeyboardRemove())
    return

def nickname_select(bot, update, user_data):
    user_data.update(username=update.message.text, type=6)
    player = Player(update.message.from_user.id, update.message.from_user.username, user_data.get('username'),
                    user_data.get('sex'), user_data.get('race'), user_data.get('fraction'), user_data.get('class'))
    player.add_to_database(conn, cursor)
    bot.send_message(chat_id=update.message.chat_id,
                     text="Вы выбрали имя <b>{0}</b>\n"
                          "И можете приступить к игре!".format(user_data.get('username')),
                     parse_mode='HTML')
    print(user_data)


def text_message(bot, update, user_data):
    pass


def loadData():
    try:
        f = open('backup/userdata', 'rb')
        dispatcher.user_data = pickle.load(f)
        f.close()
        print("Data picked up")
    except FileNotFoundError:
        logging.error("Data file not found")
    except:
        logging.error(sys.exc_info()[0])

def saveData():
    global processing
    while processing:
        time.sleep(30)
        # Before pickling
        print("Writing data, do not shutdown bot...")
        try:
            f = open('backup/userdata', 'wb+')
            pickle.dump(dispatcher.user_data, f)
            f.close()
            print("Completed")
        except:
            logging.error(sys.exc_info()[0])


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
processing = 0
# Разрываем подключение к базе данных
conn.close()