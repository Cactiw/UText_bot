# Настройки
from telegram.ext import CommandHandler, MessageHandler, Filters, Job, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
#updater = Updater(token='757939309:AAE3QMqbT8oeyZ44es-l6eSzxpy1toCf_Bk') # Токен API к Telegram        # Сам бот

#dispatcher = updater.dispatcher

import threading
import multiprocessing
import work_materials.globals as globals
import traceback

from work_materials.filters.muted_filters import *
from work_materials.filters.class_filters import *
from work_materials.filters.fraction_filters import *
from work_materials.filters.other_initiate_filters import *
from work_materials.filters.service_filters import *
from work_materials.filters.location_filters import *
from work_materials.filters.info_filters import *
from work_materials.filters.equipment_filters import *
from work_materials.filters.merchant_filters import *
from work_materials.filters.auction_filters import *
from work_materials.filters.battle_filters import *

from bin.supervisor import *
from bin.spam_resist import *
from bin.starting_player import *
from bin.save_load_user_data import *
from bin.lvl_up_player import *
from bin.auction import *
from bin.auction_checker import *
from bin.matchmaking import *
from bin.status_monitor import *

import work_materials.globals
from libs.resorses import *
from libs.equipment import *
from bin.travel_functions import *

from libs.player_matchmaking import *


sys.path.append('../')

console = logging.StreamHandler()
console.setLevel(logging.INFO)

log_file = logging.FileHandler(filename='error.log', mode='a')
log_file.setLevel(logging.ERROR)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO, handlers=[log_file, console])



logging.getLogger('').addHandler(console)

#Подключение логгирования процессов
multiprocessing.log_to_stderr()
logger = multiprocessing.get_logger()
logger.setLevel(logging.INFO)
processing = 1

work_materials.globals.processing = 1


def add_resource(bot, update, args):
    item = Resourse(int(args[0]))
    player = get_player(update.message.from_user.id)
    print("code = ", player.add_item(player.res_backpack, item, int(args[1])))


def remove_resource(bot, update, args):
    item = Resourse(int(args[0]))
    player = get_player(update.message.from_user.id)
    print("code = ", player.remove_item(player.res_backpack, item, int(args[1])))


def equip(bot, update):
    id = update.message.text.partition('_')[2]
    eqipment = Equipment(0, id, 0, 0, 0, 0, 0, 0, 0)
    if eqipment.update_from_database() is None:
        bot.send_message(chat_id=update.message.from_user.id, text="Этот предмет не найден в базе данных")
        return
    player = get_player(update.message.from_user.id)
    return_code = player.equip(eqipment)
    if return_code == 1:
        bot.send_message(chat_id=update.message.from_user.id, text="Этого предмета нет в вашем инвентаре")
        return
    if return_code == -1:
        bot.send_message(chat_id=update.message.from_user.id, text="Ошибка")
        return
    bot.send_message(chat_id = update.message.from_user.id, text = "Успешно экипировано")


def unequip(bot, update):
    id = update.message.from_user.id
    player = get_player(id)
    equipment_id = player.on_character.get(update.message.text.partition('_')[2])
    if equipment_id is None:
        bot.send_message(chat_id=update.message.from_user.id, text="Не найдено надетого предмета")
        return
    equipment = get_equipment(equipment_id)
    player.unequip(equipment)
    bot.send_message(chat_id = update.message.from_user.id, text = "Предмет успешно снят")


def merchant(bot, update, user_data):
    player = get_player(update.message.from_user.id)
    update_status('Merchant', player, user_data)
    user_data.update({'saved_status' : 'In Location'})
    show_general_buttons(bot, update, user_data)


def merchant_buy(bot, update, user_data):
    text = update.message.text
    player = get_player(update.message.from_user.id)
    if text == 'Голова':
        type = "eh"
    elif text == 'Тело':
        type = "eb"
    elif text == 'Перчатки':
        type = "es"
    elif text == 'Ноги':
        type = "ez"
    elif text == 'Средства передвижения':
        type = "em"
    elif text == 'Импланты':
        type = "ei"
    else:
        type = "e"
    location_id = player.location
    location_type = 0 if (location_id >= 14 and location_id <= 16) else 1
    request = "SELECT item_id, equipment_id, item_name, item_price FROM merchant_items WHERE location_type = '{0}' and item_type = '{1}'".format(location_type, type)
    cursor.execute(request)
    row = cursor.fetchone()
    if row is None:
        bot.send_message(chat_id=update.message.from_user.id, text="Пройдя в указанный продавцом угол, вы обнаружили"
                                                                   " лишь пыль на давно пустующих полках. Что же, может, в другой раз?")
        return
    response = "Список товаров:\n"
    while row:
        response += "\n<b>{0}</b>\n<b>💰{1}</b>\nПодробнее: /item_{2}\nКупить: /buy_{2}\n".format(row[2], row[3], row[0])
        row = cursor.fetchone()
    bot.send_message(chat_id = update.message.from_user.id, text = response, parse_mode="HTML")

def buy(bot, update, user_data):
    player = get_player(update.message.from_user.id)
    request = "SELECT equipment_id, item_price FROM merchant_items WHERE item_id = '{0}'".format(update.message.text.partition('_')[2])
    cursor.execute(request)
    row = cursor.fetchone()
    equipment = get_equipment(row[0])
    gold = player.resources.get("gold")
    if row is None or equipment is None or gold < row[1]:
        bot.send_message(chat_id=update.message.from_user.id, text="Указанный предмет не найден")
        return
    player.resources.update({"gold": gold - row[1]})
    player.add_item(player.eq_backpack, equipment, 1)
    players_need_update.put(player)
    bot.send_message(chat_id=update.message.from_user.id, text="Вы наслаждаетесь видом новой шмотки")


def matchmaking_start(bot, update, user_data):
    if user_data.get("status") != "In Location":
        bot.send_message(chat_id=update.message.chat_id, text="Сейчас вы заняты чем-то ещё")
        return

    user_data.update(matchmaking = [0, 0, 0])
    button_list = [
        InlineKeyboardButton("1 x 1", callback_data="mm 1x1"),
        InlineKeyboardButton("3 x 3", callback_data="mm 3x3"),
        InlineKeyboardButton("5 x 5", callback_data="mm 5x5")
    ]
    footer_buttons = [
        InlineKeyboardButton("Начать поиск", callback_data="mm start")
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3, footer_buttons=footer_buttons))
    bot.send_message(chat_id=update.message.chat_id, text = "Выберите настройки битвы:", reply_markup=reply_markup)

def callback(bot, update, user_data):
    mes = update.callback_query.message
    if update.callback_query.data.find("au") == 0:
        auction_callback(bot, update, user_data)
    if update.callback_query.data.find("mm") == 0:
        matchmaking = user_data.get("matchmaking")
        if update.callback_query.data == "mm start" or update.callback_query.data == "mm cancel":
            player = get_player(update.callback_query.from_user.id)

            if update.callback_query.data == "mm cancel":
                if user_data.get("status") != "Matchmaking" and user_data.get("status") != "Battle": #  TODO Как битвы будут готовы, удалить проверку на статус "Battle", сейчас используется для отладки
                    bot.send_message(chat_id=update.callback_query.from_user.id, text="Вы не находитесь в поиске битвы")
                    return
                player_matchmaking = Player_matchmaking(player, 0, matchmaking)
                matchmaking_players.put(player_matchmaking)
                bot.answerCallbackQuery(callback_query_id=update.callback_query.id,
                                        text="Подбор игроков успешно отменён", show_alert=False)
                try:
                    bot.deleteMessage(chat_id=update.callback_query.from_user.id, message_id=mes.message_id)
                except Unauthorized:
                    pass
                except BadRequest:
                    pass
                new_status = user_data.get('saved_battle_status')
                update_status(new_status, player, user_data)
                matchmaking_start(bot, update.callback_query, user_data)
                return



            #   Начало подбора игроков
            flag = 0
            for i in matchmaking:
                if i == 1:
                    flag = 1
                    break
            if flag == 0:
                bot.send_message(chat_id=update.callback_query.from_user.id, text="Необходимо выбрать хотя бы один режим")
                return

            player_matchmaking = Player_matchmaking(player, 1, matchmaking)
            #bot.answerCallbackQuery(callback_query_id=update.callback_query.id, text = "Подбор игроков успешно запущен!", show_alert = False)
            button_list = [
                InlineKeyboardButton("Отменить подбор игроков", callback_data="mm cancel")
            ]
            reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
            bot.deleteMessage(chat_id=update.callback_query.from_user.id, message_id=mes.message_id)
            bot.send_message(chat_id=update.callback_query.from_user.id, text="Подбор игроков запущен!", reply_markup=reply_markup)
            status = user_data.get("status")
            user_data.update(saved_battle_status = status) if status != 'Matchmaking' else 0
            update_status('Matchmaking', player, user_data)
            matchmaking_players.put(player_matchmaking)
            return

        # Настройки матчмейкинга битв
        #print(matchmaking)
        callback_data = update.callback_query.data
        if callback_data == "mm 1x1":
            matchmaking[0] = (matchmaking[0] + 1) % 2
        elif callback_data == "mm 3x3":
            matchmaking[1] = (matchmaking[1] + 1) % 2
        elif callback_data == "mm 5x5":
            matchmaking[2] = (matchmaking[2] + 1) % 2
        first_button_text = "{0}1 x 1".format('✅' if matchmaking[0] else "")
        second_button_text = "{0}3 x 3".format('✅' if matchmaking[1] else "")
        third_button_text = "{0}5 x 5".format('✅' if matchmaking[2] else "")
        button_list = [
            InlineKeyboardButton(first_button_text, callback_data="mm 1x1"),
            InlineKeyboardButton(second_button_text, callback_data="mm 3x3"),
            InlineKeyboardButton(third_button_text, callback_data="mm 5x5")
        ]
        footer_buttons = [
            InlineKeyboardButton("Начать поиск", callback_data="mm start")
        ]
        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3, footer_buttons=footer_buttons))
        try:
            bot.editMessageReplyMarkup(chat_id=mes.chat_id, message_id=mes.message_id, reply_markup=reply_markup)
            bot.answerCallbackQuery(callback_query_id=update.callback_query.id)
        except TelegramError:
            logging.error(traceback.format_exc)
            pass

#Фильтры на спам
dispatcher.add_handler(MessageHandler(filter_is_not_admin and filter_player_muted, ignore), group = 0)
dispatcher.add_handler(MessageHandler(filter_is_not_admin and filter_player_muted, ignore), group = 1)
dispatcher.add_handler(MessageHandler(Filters.text and filter_is_not_admin, commands_count), group = 1)

#Фильтр на старт игры
dispatcher.add_handler(CommandHandler("start", start, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_fractions, fraction_select, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_race, race_select, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_classes, class_select, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_sex_select, sex_select, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_nickname_select, nickname_select, pass_user_data=True))

#Команды для админов
dispatcher.add_handler(CommandHandler("setstatus", set_status, pass_user_data=True, filters = filter_is_admin, pass_args=True))
dispatcher.add_handler(CommandHandler("sql", sql, pass_user_data=True, filters = filter_is_admin))
dispatcher.add_handler(CommandHandler("update_player", update_player, pass_args=True, filters=filter_is_admin))
dispatcher.add_handler(CommandHandler("delete_self", delete_self, pass_user_data=True))#, filters = filter_is_admin))
dispatcher.add_handler(CommandHandler("kill_myself", delete_self, pass_user_data=True, filters = filter_is_admin))
dispatcher.add_handler(CommandHandler("showdata", show_data, pass_user_data=True, filters=filter_is_admin))
dispatcher.add_handler(CommandHandler("fasttravel", fast_travel, pass_user_data=True, filters=filter_is_admin & fast_travel_filter))
dispatcher.add_handler(CommandHandler("return", return_to_location_admin, pass_user_data=True, filters=filter_is_admin))
dispatcher.add_handler(CommandHandler("buttons", show_general_buttons, pass_user_data=True, filters=filter_is_admin))

#Фильтр для вывода информации об игроке
dispatcher.add_handler(MessageHandler(Filters.text & filter_already_in_info & filter_info & filter_not_in_lvl_up, print_player, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_in_info and filter_print_backpack, print_backpacks, pass_user_data=True))
dispatcher.add_handler(CommandHandler("me", print_player, pass_user_data=True, filters=filter_already_in_info and filter_not_in_lvl_up))
dispatcher.add_handler(CommandHandler("equipment", show_equipment))
dispatcher.add_handler(MessageHandler(Filters.text and filter_implants, show_equipment))
dispatcher.add_handler(MessageHandler(Filters.text and filter_info_return, return_from_info, pass_user_data=True))

#Фильтры для повышения уровня игрока
dispatcher.add_handler(CommandHandler("lvl_up", lvl_up, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_lvl_up_skill, lvl_up_skill, pass_user_data=True))
dispatcher.add_handler(CommandHandler("lvl_up_points", choose_points, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_lvl_up_points, lvl_up_points, pass_user_data=True))

#Фильтр для перемещения
dispatcher.add_handler(MessageHandler(Filters.text and location_filter and travel_filter, travel, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and choosing_way_filter, choose_way, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_return_to_location, return_to_location, pass_user_data=True))

#Фильтры для торговца
dispatcher.add_handler(MessageHandler(Filters.text and filter_merchant, merchant, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_merchant_buy, merchant_buy, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_return_from_merchant, return_from_info, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_buy_equipment, buy, pass_user_data=True))


#Фильтры для аукциона
dispatcher.add_handler(MessageHandler(Filters.text and filter_auction, auction, pass_user_data=False))
dispatcher.add_handler(MessageHandler(Filters.text and filter_create_lot, create_lot, pass_user_data=False))
dispatcher.add_handler(MessageHandler(Filters.text and filter_cancel_lot, cancel_lot, pass_user_data=False))
dispatcher.add_handler(MessageHandler(Filters.text and filter_bet, bet, pass_user_data=False))
dispatcher.add_handler(MessageHandler(Filters.text and filter_lots, lots, pass_user_data=False))
dispatcher.add_handler(MessageHandler(Filters.text and filter_my_lots, my_lots, pass_user_data=False))
dispatcher.add_handler(MessageHandler(Filters.text and filter_my_bids, my_bids, pass_user_data=False))



dispatcher.add_handler(CommandHandler("matchmaking_start", matchmaking_start, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_start_battle, matchmaking_start, pass_user_data=True))


dispatcher.add_handler(CallbackQueryHandler(callback, pass_update_queue=False, pass_user_data=True))







#Команды для добавления и удаления предметов
dispatcher.add_handler(CommandHandler("add_resource", add_resource, pass_user_data=False, pass_args=True))
dispatcher.add_handler(CommandHandler("remove_resource", remove_resource, pass_user_data=False, pass_args=True))

dispatcher.add_handler(MessageHandler(Filters.text and filter_equip, equip, pass_user_data=False))
dispatcher.add_handler(MessageHandler(Filters.text and filter_unequip, unequip, pass_user_data=False))


#-------------------

def text_message(bot, update, user_data):
    bot.send_message(chat_id=update.message.chat_id, text="Некорректный ввод")
    show_general_buttons(bot, update, user_data)


dispatcher.add_handler(MessageHandler(Filters.text, text_message, pass_user_data = True))

#-------------------

loadData()
parse_travel_jobs()
#sys.stdout.flush()

processes = []

save_user_data = threading.Thread(target=saveData, name="Save User Data")
save_user_data.start()
processes.append(save_user_data)
#Запуск процесса обновления игроков в бд

updating_to_database = Process(target = players_update, args = (players_need_update,), name = "Database_cloud_updating")
updating_to_database.start()
processes.append(updating_to_database)

auction_checking = Process(target = auction_checker, args = (), name = "Auction checking")
auction_checking.start()
processes.append(auction_checking)

matchmaking = Process(target = matchmaking, args=(), name="Matchmaking")
matchmaking.start()
processes.append(matchmaking)

spam_zeroing = threading.Thread(target = zeroing, args=(), name="Spam zeroing")
spam_zeroing.start()
processes.append(spam_zeroing)

status_monitor = threading.Thread(target = status_monitor, args = (), name = "Player Status Monitor")
status_monitor.start()
processes.append(status_monitor)

supervisor = threading.Thread(target = process_monitor, args = (processes,), name = "Supervisor")
supervisor.start()

updater.start_polling(clean=False)

# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
# Разрываем подключение к базе данных
work_materials.globals.processing = 0
conn.close()
players_need_update.put(None)
statuses.put(None)
try:
    updating_to_database.join()
except:
    pass

try:
    auction_checking.join()
except:
    pass
