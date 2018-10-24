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
from work_materials.class_filters import *
from work_materials.fraction_filters import *

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
    print(user_data)
    user_data.update(type = 1)
    print(user_data)
    button_list = [
        KeyboardButton("Люди"),
        KeyboardButton("Орки"),
        KeyboardButton("Эльфы")
    ]
    reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=3))
    bot.send_message(chat_id=update.message.chat_id, text="Выберите фракцию, за которую вы будете сражаться!", reply_markup = reply_markup)
    return
    #player = Player(update.message.chat_id, update.message.user_from.username, update.message.user_from.username, )

def fraction_select(bot, update, user_data):
    type = user_data.get('type')
    if type is not None:
        if type is 1:
            user_data.update({'fraction': update.message.text, 'type': 2})

            button_list = [
                KeyboardButton("Воин"),
                KeyboardButton("Маг"),
                KeyboardButton("Лучник"),
                KeyboardButton("Клирик"),
            ]
            reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=2))

            bot.send_message(chat_id=update.message.chat_id, text="Вы выбрали фракцию <b>{0}</b>\n"
                                                                  "Теперь необходимо выбрать класс!".format(
                user_data.get('fraction')), parse_mode='HTML', reply_markup=reply_markup)

def class_select(bot, update, user_data):
    type = user_data.get('type')
    if type is not None:
        if type is 2:
            user_data.update({'class' : update.message.text, 'type' : 3})


def text_message(bot, update, user_data):
    print(user_data, 'type' in user_data)
    type = user_data.get('type')
    if type is not None:
        if type is 1:
            user_data.update(username = update.message.text, type = 2)
            bot.send_message(chat_id=update.message.chat_id, text="Вы выбрали имя <b>{0}</b>\n"
                                                                  "Теперь необходимо выбрать класс!".format(user_data.get('username')), parse_mode = 'HTML')




dispatcher.add_handler(CommandHandler("start", start, pass_user_data=True))

dispatcher.add_handler(MessageHandler(filter_classes, class_select, pass_user_data=True))

dispatcher.add_handler(MessageHandler(Filters.text, text_message, pass_user_data=True))



updater.start_polling(clean=True)

# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
# Разрываем подключение.
#conn.close()