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

from bin.service_commands import *
from bin.starting_player import *
from bin.save_load_user_data import *
from bin.lvl_up_player import *

import work_materials.globals
from libs.resorses import *
from libs.equipment import *
from libs.myJob import MyJob

sys.path.append('../')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
#Подключение логгирования процессов
multiprocessing.log_to_stderr()
logger = multiprocessing.get_logger()
logger.setLevel(logging.INFO)

work_materials.globals.processing = 1


def move_player(bot, job):
    player = job.context.get('player')
    user_data = job.context.get('user_data')
    update_status('In Location', player, user_data)
    update_location(job.context.get('location_id'), player, user_data)
    print(player.nickname, "Переместился в новую локацию -", player.location)
    players_need_update.put(player)
    show_general_buttons(bot, job.context.get('update'), user_data)


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
    
    
def travel(bot, update, user_data):
    player = get_player(update.message.from_user.id)
    current_location = locations.get(player.location)
    paths = current_location.roads
    path_buttons = []
    for i in paths:
        path_buttons.append(KeyboardButton(locations.get(i).name))
    path_buttons.append(KeyboardButton("Назад"))
    road_buttons = ReplyKeyboardMarkup(build_menu(path_buttons, n_cols=2), resize_keyboard=True, one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Вы в локации: {0}".format(current_location.name), reply_markup=road_buttons)
    update_status('Choosing way', player, user_data)


def choose_way(bot, update, user_data):
    if update.message.text == 'Назад':
        update_status('In Location', players.get(update.message.from_user.id), user_data)
        show_general_buttons(bot, update, user_data)
        return
    player = get_player(update.message.from_user.id)
    current_location = locations.get(player.location)
    paths = current_location.roads
    loc_name = update.message.text
    new_loc_id = 0
    for i in paths.keys():
        tmp_location = i
        if locations.get(tmp_location).name == loc_name:
            new_loc_id = tmp_location
            break
    if new_loc_id == 0:
        work_materials.globals.logging.error('ERROR: NO SUCH ID bot.py in choose_way, id = 0')
    else:
        update_status('Traveling', player, user_data)
        bot.send_message(chat_id=update.message.chat_id, text="Вы отправились в локацию: {0}, до нее идти {1} минут".format(locations.get(new_loc_id).name, paths.get(new_loc_id)), reply_markup=traveling_buttons)
        #TODO понять, почему не работает с орками и эльфами
        contexts = {'chat_id': update.message.chat_id, 'location_id': new_loc_id, 'player': player,
                   'update': update, 'user_data': user_data}
        if filter_is_admin(update.message):
            bot.send_message(chat_id=update.message.chat_id, text="Вы можете использовать /fasttravel")
        user_data.update({'new_location': new_loc_id})
        tmp_job = job.run_once(move_player, paths.get(new_loc_id) * 60, context=contexts)
        j = MyJob(tmp_job, paths.get(new_loc_id) * 60)
        travel_jobs.update({player.id: j})
        return


def fast_travel(bot, update, user_data):
    player = get_player(update.message.from_user.id)
    j = travel_jobs.get(player.id)
    print(j.get_time_left())
    if j is not None:
        j.job.schedule_removal()
        j.job.run(bot)

def return_to_location_admin(bot, update, user_data):
    player = get_player(update.message.from_user.id)
    update_status('In Location', player, user_data)
    update_location(player.location, player, user_data)
    j = travel_jobs.get(player.id)
    bot.send_message(chat_id=update.message.chat_id,text="Вы вернулись в локацию: {0}".format(locations.get(player.location).name))
    show_general_buttons(bot, update, user_data)
    if j is None:
        return
    j.job.schedule_removal()


def return_to_location(bot, update, user_data):
    player = get_player(update.message.from_user.id)
    j = travel_jobs.get(player.id)
    if j is None:
        bot.send_message(chat_id=update.message.chat_id, text="Вы стоите на месте, наверное вы заблудились /return")
        return
    j.job.schedule_removal()
    j.swap_time()
    new_loc_id = user_data.get('location')
    tmp_loc = user_data.get('location')
    user_data.update({'location': user_data.get('new_location')})
    user_data.update({'new_location': tmp_loc})
    sec = int(j.get_time_left()%60)
    time_str = '' + str(int(j.get_time_left()//60)) + ':' + ('0' if sec < 10 else '') + str(sec)
    location_name = locations.get(new_loc_id).name
    user_data.update({'location_name': location_name})
    contexts = {'chat_id': update.message.chat_id, 'location_id': new_loc_id, 'player': player,
                'update': update, 'user_data': user_data}
    bot.send_message(chat_id=update.message.chat_id, text="Вы решили вернуться в локацию {0}, осталось идти: <b>{1}</b>".format(
        location_name, time_str
    ), parse_mode='HTML')
    j.job = job.run_once(move_player, j.get_time_left(), context=contexts)



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
