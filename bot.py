# Настройки
from telegram.ext import CommandHandler, MessageHandler, Filters, Job
#updater = Updater(token='757939309:AAE3QMqbT8oeyZ44es-l6eSzxpy1toCf_Bk') # Токен API к Telegram        # Сам бот

#dispatcher = updater.dispatcher

import threading
import multiprocessing

from work_materials.filters.class_filters import *
from work_materials.filters.fraction_filters import *
from work_materials.filters.other_initiate_filters import *
from work_materials.filters.service_filters import *
from work_materials.filters.location_filters import *
from work_materials.filters.info_filters import *
from work_materials.filters.equipment_filters import *
from work_materials.filters.merchant_filters import *

from bin.service_commands import *
from bin.starting_player import *
from bin.save_load_user_data import *
from bin.lvl_up_player import *

import work_materials.globals
from libs.resorses import *
from libs.equipment import *
from libs.myJob import MyJob
from bin.travel_functions import *

sys.path.append('../')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
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
    if location_id >= 14 and location_id <= 16:
        location_type = 0
    else:
        location_type = 1
    request = "SELECT item_id, equipment_id, item_name, item_price FROM merchant_items WHERE location_type = '{0}' and item_type = '{1}'".format(location_type, type)
    print(request)
    cursor.execute(request)
    row = cursor.fetchone()
    print(row)
    if row is None:
        bot.send_message(chat_id=update.message.from_user.id, text="Пройдя в указанный продавцом угол, вы обнаружили"
                                                                   " лишь пыль на давно пустующих полках. Что же, может, в другой раз?")
        return
    update_status('Merchant_buy', player, user_data)
    response = "Список товаров:\n"
    while row:
        response += "\n<b>{0}</b>\n<b>💰{1}</b>\nПодробнее: /item_{2}\nКупить: /buy_{2}\n".format(row[2], row[3], row[0])
        row = cursor.fetchone()
    bot.send_message(chat_id = update.message.from_user.id, text = response, parse_mode="HTML")
    show_general_buttons(bot, update, user_data)


def buy(bot, update, user_data):
    player = get_player(update.message.from_user.id)
    request = "SELECT equipment_id, item_price FROM merchant_items WHERE item_id = '{0}'".format(update.message.text.partition('_')[2])
    cursor.execute(request)
    row = cursor.fetchone()
    if row is None:
        bot.send_message(chat_id=update.message.from_user.id, text="Указанный предмет не найден")
        return
    equipment = get_equipment(row[0])
    if equipment is None:
        bot.send_message(chat_id=update.message.from_user.id, text="Указанный предмет не найден")
        return
    gold = player.resources.get("gold")
    if player.resources.get("gold") < row[1]:
        bot.send_message(chat_id=update.message.from_user.id, text="У вас недостаточно золота")
        return
    player.resources.update({"gold" : gold - row[1]})
    player.add_item(player.eq_backpack, equipment, 1)
    players_need_update.put(player)
    bot.send_message(chat_id=update.message.from_user.id, text="Вы наслаждаетесь видом новой шмотки")


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
dispatcher.add_handler(CommandHandler("delete_self", delete_self, pass_user_data=True, filters = filter_is_admin))
dispatcher.add_handler(CommandHandler("kill_myself", delete_self, pass_user_data=True, filters = filter_is_admin))
dispatcher.add_handler(CommandHandler("showdata", show_data, pass_user_data=True, filters=filter_is_admin))
dispatcher.add_handler(CommandHandler("fasttravel", fast_travel, pass_user_data=True, filters=filter_is_admin & fast_travel_filter))
dispatcher.add_handler(CommandHandler("return", return_to_location_admin, pass_user_data=True, filters=filter_is_admin))
dispatcher.add_handler(CommandHandler("buttons", show_general_buttons, pass_user_data=True, filters=filter_is_admin))

#Фильтр для вывода информации об игроке
dispatcher.add_handler(MessageHandler(Filters.text and filter_info, print_player, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_in_info and filter_print_backpack, print_backpacks, pass_user_data=True))
dispatcher.add_handler(CommandHandler("me", print_player, pass_user_data=True))
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
dispatcher.add_handler(MessageHandler(Filters.text and filter_return_to_merchant, merchant, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_buy_equipment, buy, pass_user_data=True))






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
threading.Thread(target=saveData).start()
updater.start_polling(clean=False)

#Запуск процесса обновления игроков в бд

updating_to_database = Process(target = players_update, args = (players_need_update,), name = "Database_cloud_updating").start()

# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
# Разрываем подключение к базе данных
work_materials.globals.processing = 0
conn.close()
players_need_update.put(None)
try:
    updating_to_database.join()
except:
    pass
