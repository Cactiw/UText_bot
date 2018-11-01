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
import multiprocessing
from multiprocessing import Process, Queue

from libs import player
from work_materials.class_filters import *
from work_materials.fraction_filters import *
from work_materials.other_initiate_filters import *
from work_materials.service_filters import *

from bin.service_commands import *
from bin.starting_player import *
from bin.save_load_user_data import *

import work_materials.globals


work_materials.globals.processing = 1

players = {}
players_need_update = Queue()

def players_update(q):
    try:
        data = q.get()
        while data is not None:
            data.update_to_database(conn, cursor)
            data = q.get()
        return
    except KeyboardInterrupt:
        if q.empty:
            print("No users need to be updated, return")
            return
        print("Writing all updated users to database, wait...")
        while not q.empty():
            data = q.get()
            data.update_to_database(conn, cursor)
        print("All users are in database and updated")
        return

def update_status(status, id, user_data):
    player = get_player(id)
    player.status = status
    players.update({id: player})
    user_data.update({"status": status})

def get_player(id):
    player = players.get(id)
    if player is not None:
        return player
    player = Player(id, 0, 0, 0, 0, 0, 0)
    if player.update_from_database(cursor) is None:
        return None
    players.update({player.id : player})
    return player

def choose_points(bot, update, user_data):
    id = update.message.from_user.id
    player = get_player(id)
    if(player is None):
        return
    free_points = player.free_points
    if(free_points < 0):
        player.free_points = 0
        free_points = 0
    if(free_points == 0):
        bot.send_message(chat_id = update.message.chat_id, text = "У вас нет свободных очков\n\n"
                                                                  "Выносливость - <b>{0}</b>\nБроня - <b>{1}</b>\n"
                                                                  "Сила - <b>{2}</b>\nЛовкость - <b>{3}</b>\n"
                                                                  "Очки маны - <b>{4}</b>".format(
            player.stats.get("endurance"), player.stats.get("armor"),
            player.stats.get("power"), player.stats.get("agility"),
            player.stats.get("mana_points")),
                         parse_mode = "HTML", reply_markup = ReplyKeyboardRemove())
        players.update({id: player})
        players_need_update.put(player)
        update_status("Rest", id, user_data)
        return

    update_status("Lvl_up_points", id, user_data)
    button_list = [
        KeyboardButton("Выносливость"),
        KeyboardButton("Броня"),
        KeyboardButton("Сила"),
        KeyboardButton("Ловкость"),
        KeyboardButton("Очки маны"),
        KeyboardButton("Готово")
    ]
    buttons = ReplyKeyboardMarkup(build_menu(button_list, n_cols=2), resize_keyboard=True, one_time_keyboard=False)


    if free_points == 1:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Вы можете улучшить <b>1</b> характеристику\n\nВыберите характеристику, которую хотите улучшить\n"
                              "Выносливость - <b>{0}</b>\nБроня - <b>{1}</b>\n"
                              "Сила - <b>{2}</b>\nЛовкость - <b>{3}</b>\n"
                              "Очки маны - <b>{4}</b>".format(player.stats.get("endurance"), player.stats.get("armor"),
                                                       player.stats.get("power"), player.stats.get("agility"),
                                                       player.stats.get("mana_points")),
                         parse_mode='HTML', reply_markup=buttons)
    elif free_points >= 2 or free_points <= 4:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Вы можете улучшить <b>{5}</b> характеристики\n\nВыберите характеристику, которую хотите улучшить\n"
                              "Выносливость - <b>{0}</b>\nБроня - <b>{1}</b>\n"
                              "Сила - <b>{2}</b>\nЛовкость - <b>{3}</b>\n"
                              "Очки маны - <b>{4}</b>".format(player.stats.get("endurance"), player.stats.get("armor"),
                                                       player.stats.get("power"), player.stats.get("agility"),
                                                       player.stats.get("mana_points"), free_points),
                         parse_mode='HTML', reply_markup=buttons)
    elif free_points >= 5:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Вы можете улучшить <b>{5}</b> характеристик\n\nВыберите характеристику, которую хотите улучшить\n"
                              "Выносливость - <b>{0}</b>\nБроня - <b>{1}</b>\n"
                              "Сила - <b>{2}</b>\nЛовкость - <b>{3}</b>\n"
                              "Очки маны - <b>{4}</b>".format(player.stats.get("endurance"), player.stats.get("armor"),
                                                       player.stats.get("power"), player.stats.get("agility"),
                                                       player.stats.get("mana_points"), free_points),
                         parse_mode='HTML', reply_markup=buttons)
    players.update({id: player})
    players_need_update.put(player)

def lvl_up_points(bot, update, user_data):
    id = update.message.from_user.id
    player = get_player(id)
    if player is None:
        return
    if update.message.text == "Готово":
        update_status("Rest", id, user_data)
        return
    else:
        player.lvl_up_point(update.message.text)
        player.free_points -= 1
        players.update({id: player})
        players_need_update.put(player)
        if(update.message.text == "Очки маны"):
            bot.send_message(chat_id=update.message.chat_id,
                             text="Увеличины <b>{0}</b>".format(update.message.text),
                             parse_mode='HTML')
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text="Улучшена <b>{0}</b>".format(update.message.text),
                             parse_mode='HTML')
        choose_points(bot, update, user_data)

def choose_skill(bot, update, user_data): #Сюда игрок попадает при нажатии /lvl_up, ему предлагается выбрать скилл, который он хочет вкачать
    id = update.message.from_user.id
    player = get_player(id)
    if player is None:
        return
    free_skill = player.free_skill_points
    if(free_skill < 0) :
        player.free_skill_points = 0
        free_skill = 0
    if free_skill == 0:
        bot.send_message(chat_id = update.message.chat_id,
                         text = "У вас нет очков навыков\n\n"
                                 "Первый навык - {0}-го уровня\nВторой навык - {1}-го уровня\n"
                                 "Третий навык - {2}-го уровня\nЧетвертый навык - {3}-го уровня\n"
                                 "Пятый навык - {4}-го уровня".format( player.first_skill_lvl, player.second_skill_lvl,
                                                                        player.third_skill_lvl, player.fourth_skill_lvl,
                                                                        player.fifth_skill_lvl),
                         reply_markup = ReplyKeyboardRemove()
                         )
        #player.status = "Lvl_up_point"
        #user_data.update({"status": "Lvl_up_points"})
        update_status("Lvl_up_points", id, user_data)
        players.update({id: player})
        players_need_update.put(player)
        choose_points(bot, update, user_data)
        return

    update_status("Lvl_up_skill", id, user_data)
    button_list = [
        KeyboardButton("1"),
        KeyboardButton("2"),
        KeyboardButton("3"),
        KeyboardButton("4"),
        KeyboardButton("5"),
        KeyboardButton("Готово")
    ]
    buttons = ReplyKeyboardMarkup(build_menu(button_list, n_cols=2), resize_keyboard=True, one_time_keyboard = False)

    if free_skill == 1:
        bot.send_message(chat_id=update.message.chat_id,
                        text = "Вы можете улучшить <b>1</b> навык\n\nВыберите навык, который хотите улучшить\n\n"
                               "Первый навык - {0}-го уровня\nВторой навык - {1}-го уровня\n"
                               "Третий навык - {2}-го уровня\nЧетвертый навык - {3}-го уровня\n"
                               "Пятый навык - {4}-го уровня".format(player.first_skill_lvl, player.second_skill_lvl,
                                                                    player.third_skill_lvl, player.fourth_skill_lvl,
                                                                    player.fifth_skill_lvl),
                        parse_mode = 'HTML', reply_markup = buttons)
    elif free_skill >= 2 and free_skill <= 4:
        bot.send_message(chat_id=update.message.chat_id,
                        text="Вы можете улучшить <b>{0}</b> навыкa\n\nВыберите навык, который хотите улучшить\n\n"
                             "Первый навык - {1}-го уровня\nВторой навык - {2}-го уровня\n"
                             "Третий навык - {3}-го уровня\nЧетвертый навык - {4}-го уровня\n"
                             "Пятый навык - {5}-го уровня".format(free_skill, player.first_skill_lvl,
                                                                  player.second_skill_lvl, player.third_skill_lvl,
                                                                  player.fourth_skill_lvl, player.fifth_skill_lvl),
                        parse_mode='HTML', reply_markup = buttons)
    elif free_skill >= 5:
        bot.send_message(chat_id=update.message.chat_id,
                        text="Вы можете улучшить <b>{0}</b> навыков\n\nВыберите навык, который хотите улучшить\n\n"
                             "Первый навык - {1}-го уровня\nВторой навык - {2}-го уровня\n"
                             "Третий навык - {3}-го уровня\nЧетвертый навык - {4}-го уровня\n"
                             "Пятый навык - {5}-го уровня".format(free_skill, player.first_skill_lvl,
                                                                  player.second_skill_lvl, player.third_skill_lvl,
                                                                  player.fourth_skill_lvl, player.fifth_skill_lvl),
                        parse_mode='HTML', reply_markup = buttons)
    players.update({id: player})
    players_need_update.put(player)

def lvl_up_skill(bot, update, user_data):
    id = update.message.from_user.id
    player = get_player(id)
    if player is None:
        return
    if update.message.text == "Готово":
        update_status("Lvl_up_points", id, user_data)
        bot.send_message(chat_id = update.message.from_user.id, text = "", reply_markup = ReplyKeyboardRemove())
        choose_points(bot, update, user_data)
    else:
        player.lvl_up_skill(update.message.text)
        player.free_skill_points -= 1
        players.update({id : player})
        players_need_update.put(player)
        bot.send_message(chat_id = update.message.chat_id, text = "Улучшен <b>{0}</b> скилл".format(update.message.text), parse_mode = 'HTML')
        choose_skill(bot, update, user_data)

def print_player(bot, update, user_data):
    id = update.message.from_user.id
    player = get_player(id)
    if(player is None):
        return
    bot.send_message(chat_id=update.message.chat_id, text="Ник - <b>{0}</b>\nПол - <b>{1}</b>\nРаса - <b>{2}</b>\nФракция - <b>{3}</b>\nClass - <b>{4}</b>"
                                                          "\n\nStatus - <b>{5}</b>\n\nexp = <b>{6}</b>\nlvl = <b>{7}</b>\nFree_points = <b>{8}</b>"
                                                          "\nFree_skill_points = <b>{9}</b>\nFatigue = <b>{10}</b>\n\n"
                                                          "Первый навык - <b>{11}</b>-го уровня\nВторой навык - <b>{12}</b>-го уровня"
                                                          "\nТретий навык - <b>{13}</b>-го уровня\n"
                                                          "Четвертый навык - <b>{14}</b>-го уровня\n"
                                                          "Пятый навык - <b>{15}</b>-го уровня\n\nВыносливость - <b>{16}</b>\n"
                                                          "Броня - <b>{17}</b>\nСила - <b>{18}</b>\nЛовкость - <b>{19}</b>\n"
                                                          "Очки маны - <b>{20}</b>".format(
        player.nickname, player.sex, player.race, player.fraction, 
        player.game_class, player.status, player.exp, player.lvl, 
        player.free_points, player.free_skill_points, player.fatigue, 
        player.first_skill_lvl, player.second_skill_lvl, player.third_skill_lvl, 
        player.fourth_skill_lvl, player.fifth_skill_lvl, player.stats["endurance"], 
        player.stats["armor"], player.stats["power"], player.stats["agility"], player.stats["mana_points"]),
        parse_mode="HTML")


dispatcher.add_handler(CommandHandler("start", start, pass_user_data = True))

dispatcher.add_handler(CommandHandler("me", print_player, pass_user_data = True))

dispatcher.add_handler(MessageHandler(Filters.text and filter_classes, class_select, pass_user_data = True))

dispatcher.add_handler(MessageHandler(Filters.text and filter_fractions, fraction_select, pass_user_data = True))

dispatcher.add_handler(MessageHandler(Filters.text and filter_sex_select, sex_select, pass_user_data = True))

dispatcher.add_handler(MessageHandler(Filters.text and filter_nickname_select, nickname_select, pass_user_data = True))

dispatcher.add_handler(CommandHandler("lvl_up", choose_skill, pass_user_data = True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_lvl_up_skill, lvl_up_skill, pass_user_data = True))
dispatcher.add_handler(CommandHandler("lvl_up_points", choose_points, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_lvl_up_points, lvl_up_points, pass_user_data=True))

dispatcher.add_handler(CommandHandler("sql", sql, pass_user_data=True, filters = filter_is_admin))


#-------------------

def text_message(bot, update, user_data):
    print(user_data)
    bot.send_message(chat_id=update.message.chat_id, text = "Некорректный ввод")

dispatcher.add_handler(MessageHandler(Filters.text, text_message, pass_user_data = True))



loadData()
#print(dispatcher.user_data)
threading.Thread(target=saveData).start()
updater.start_polling(clean=False)

#Запуск процесса обновления игроков в бд
multiprocessing.log_to_stderr()
logger = multiprocessing.get_logger()
logger.setLevel(logging.INFO)

updating_to_database = Process(target = players_update, args = (players_need_update,))
updating_to_database.start()

# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
work_materials.globals.processing = 0
# Разрываем подключение к базе данных
conn.close()
players_need_update.put(None)
updating_to_database.join()