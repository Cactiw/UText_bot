# Настройки
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler

import threading
import multiprocessing
import work_materials.globals as globals
import sys
from multiprocessing import Process

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
from work_materials.filters.group_filters import group_kick_filter
from work_materials.filters.farm_filters import farm_filter

from bin.supervisor import *
from bin.spam_resist import *
from bin.starting_player import *
from bin.save_load_user_data import *
from bin.lvl_up_player import *
from bin.auction import *
from bin.auction_checker import *
from bin.initiate_matchmaking import matchmaking_start, matchmaking_callback
from bin.matchmaking import matchmaking
from bin.interprocess_monitor import interprocess_monitor, interprocess_queue
from bin.merchant import *
from bin.battle_group import group_invite, group_info, group_kick, group_leave, battle_group_callback
from bin.equip_items import add_resource, remove_resource, equip, unequip
from bin.farm import farm

import work_materials.globals
from bin.travel_functions import *
from bin.battle_processing import choose_enemy_target, choose_friendly_target, set_target, battle_cancel_choosing, \
                                    battle_skip_turn, battle_count, send_waiting_msg, put_in_pending_battles_from_queue, \
                                    send_message_dead, kick_out_players, set_skill_on_enemy_team, set_skill_on_ally_team, \
                                    battle_stunned
from bin.ai_processing import bots_processing

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


def callback(bot, update, user_data):
    if update.callback_query.data.find("au") == 0:
        auction_callback(bot, update, user_data)
        return
    if update.callback_query.data.find("mm") == 0:
        matchmaking_callback(bot, update, user_data)
        return
    if update.callback_query.data.find("bg") == 0:
        battle_group_callback(bot, update, user_data)
        return


def check_player_lvl(bot, update):
    player = get_player(update.message.from_user.id)
    player.lvl_check()

#Фильтры на спам и бан
dispatcher.add_handler(MessageHandler(filter_is_banned, ignore))
dispatcher.add_handler(MessageHandler(~filter_in_white_list, ignore))
dispatcher.add_handler(MessageHandler(filter_is_not_admin & filter_player_muted, ignore), group = 0)
dispatcher.add_handler(MessageHandler(filter_is_not_admin & filter_player_muted, ignore), group = 1)
dispatcher.add_handler(MessageHandler(Filters.text & filter_is_not_admin, commands_count), group = 1)

#Фильтры на битву
dispatcher.add_handler(MessageHandler(Filters.text & filter_battle_dead, send_message_dead, pass_user_data=False))
dispatcher.add_handler(MessageHandler(Filters.text & filter_battle_waiting_update, send_waiting_msg, pass_user_data=False))
dispatcher.add_handler(MessageHandler(Filters.text & filter_battle_cancel, battle_cancel_choosing, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text & ~filter_is_not_stunned, battle_stunned, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text & filter_status_battle & filter_battle_skip_turn, battle_skip_turn, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text & filter_use_skill_on_enemy & filter_status_battle, choose_enemy_target, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text & filter_use_skill_on_ally & filter_status_battle, choose_friendly_target, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text & filter_use_skill_on_anyone & filter_status_battle, choose_friendly_target, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text & filter_use_skill_on_enemy_team & filter_status_battle, set_skill_on_enemy_team, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text & filter_use_skill_on_ally_team & filter_status_battle, set_skill_on_ally_team, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text & filter_status_choosing_target, set_target, pass_user_data=True))

#Фильтры на группы
dispatcher.add_handler(CommandHandler("group_invite", group_invite, pass_user_data=True))
dispatcher.add_handler(CommandHandler("group_info", group_info, pass_user_data=True))
dispatcher.add_handler(CommandHandler("group_leave", group_leave, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.command & group_kick_filter, group_kick, pass_user_data=True))

#Фильтр на старт игры
dispatcher.add_handler(CommandHandler("start", start, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text & filter_fractions, fraction_select, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text & filter_race, race_select, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text & filter_classes, class_select, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text & filter_sex_select, sex_select, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text & filter_nickname_select, nickname_select, pass_user_data=True))

#Команды для админов
dispatcher.add_handler(CommandHandler("setstatus", set_status, pass_user_data=True, filters = filter_is_admin, pass_args=True))
dispatcher.add_handler(CommandHandler("sql", sql, pass_user_data=True, filters = filter_is_admin))
dispatcher.add_handler(CommandHandler("update_player", update_player, pass_args=True, filters=filter_is_admin))
dispatcher.add_handler(CommandHandler("delete_self", delete_self, pass_user_data=True))#, filters = filter_is_admin))
dispatcher.add_handler(CommandHandler("kill_myself", delete_self, pass_user_data=True, filters = filter_is_admin))
dispatcher.add_handler(CommandHandler("showdata", show_data, pass_user_data=True))#, filters=filter_is_admin))
dispatcher.add_handler(CommandHandler("fasttravel", fast_travel, pass_user_data=True, filters=filter_is_admin & fast_travel_filter))
dispatcher.add_handler(CommandHandler("return", return_to_location_admin, pass_user_data=True)) #filters=filter_is_admin))
dispatcher.add_handler(CommandHandler("buttons", show_general_buttons, pass_user_data=True, filters=filter_is_admin))

#Фильтр для вывода информации об игроке
dispatcher.add_handler(MessageHandler(Filters.text & filter_already_in_info & filter_info & filter_not_in_lvl_up, print_player, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text & filter_in_info & filter_print_backpack, print_backpacks, pass_user_data=True))
dispatcher.add_handler(CommandHandler("me", print_player, pass_user_data=True, filters=filter_already_in_info & filter_not_in_lvl_up))
dispatcher.add_handler(CommandHandler("equipment", show_equipment))
dispatcher.add_handler(MessageHandler(Filters.text & filter_implants, show_equipment))
dispatcher.add_handler(MessageHandler(Filters.text & filter_info_return, return_from_info, pass_user_data=True))

#Фильтры для повышения уровня игрока
dispatcher.add_handler(CommandHandler("lvl_up", lvl_up, pass_user_data=True))
dispatcher.add_handler(CommandHandler("lvl_check", check_player_lvl))
dispatcher.add_handler(MessageHandler(Filters.text & filter_lvl_up_skill, lvl_up_skill, pass_user_data=True))
dispatcher.add_handler(CommandHandler("lvl_up_points", choose_points, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text & filter_lvl_up_points, lvl_up_points, pass_user_data=True))

#Фильтр для перемещения
dispatcher.add_handler(MessageHandler(Filters.text & location_filter & travel_filter, travel, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text & choosing_way_filter, choose_way, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text & filter_return_to_location, return_to_location, pass_user_data=True))

#Фильтры для торговца
dispatcher.add_handler(MessageHandler(Filters.text & filter_merchant, merchant, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text & filter_merchant_buy, merchant_buy, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text & filter_return_from_merchant, return_from_merchant, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.command & filter_buy_equipment, buy, pass_user_data=True))

#Фильтры для гринда
dispatcher.add_handler(MessageHandler(Filters.text & farm_filter, farm, pass_user_data=True))


#Фильтры для аукциона
dispatcher.add_handler(MessageHandler(Filters.text & filter_auction, auction, pass_user_data=False))
dispatcher.add_handler(MessageHandler(Filters.command & filter_create_lot, create_lot, pass_user_data=False))
dispatcher.add_handler(MessageHandler(Filters.command & filter_cancel_lot, cancel_lot, pass_user_data=False))
dispatcher.add_handler(MessageHandler(Filters.command & filter_bet, bet, pass_user_data=False))
dispatcher.add_handler(MessageHandler(Filters.command & filter_lots, lots, pass_user_data=False))
dispatcher.add_handler(MessageHandler(Filters.command & filter_my_lots, my_lots, pass_user_data=False))
dispatcher.add_handler(MessageHandler(Filters.command & filter_my_bids, my_bids, pass_user_data=False))

dispatcher.add_handler(CommandHandler("matchmaking_start", matchmaking_start, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text & filter_start_battle, matchmaking_start, pass_user_data=True))


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

interprocess_monitor = threading.Thread(target = interprocess_monitor, args = (), name = "Interprocess Monitor")
interprocess_monitor.start()
processes.append(interprocess_monitor)

battle_processing = Process(target= battle_count, args=(), name= "Battle Processing")
battle_processing.start()
processes.append(battle_processing)

ai_processing = Process(target= bots_processing, args=(), name= "AI Processing")
ai_processing.start()
processes.append(ai_processing)

updating_pending_battles = threading.Thread(target=put_in_pending_battles_from_queue, args=(), name="Updating pending battles")
updating_pending_battles.start()
processes.append(updating_pending_battles)

kicking_out_thread = threading.Thread(target=kick_out_players, args=(), name="Kicking players out of battle")
kicking_out_thread.start()
processes.append(kicking_out_thread)

supervisor = threading.Thread(target = process_monitor, args = (processes,), name = "Supervisor")
supervisor.start()

updater.start_polling(clean=False)

# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
# Разрываем подключение к базе данных
work_materials.globals.processing = 0
conn.close()
players_need_update.put(None)
interprocess_queue.put(None)
treated_battles.put(None)
