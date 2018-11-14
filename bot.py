# Настройки
from telegram.ext import CommandHandler, MessageHandler, Filters
#updater = Updater(token='757939309:AAE3QMqbT8oeyZ44es-l6eSzxpy1toCf_Bk') # Токен API к Telegram        # Сам бот

#dispatcher = updater.dispatcher

import threading
import multiprocessing
from multiprocessing import Process, Queue

from work_materials.filters.class_filters import *
from work_materials.filters.fraction_filters import *
from work_materials.filters.other_initiate_filters import *
from work_materials.filters.service_filters import *
from work_materials.filters.location_filters import *
from work_materials.player_service import *

from bin.service_commands import *
from bin.starting_player import *
from bin.save_load_user_data import *
from bin.show_general_buttons import show_general_buttons
from bin.lvl_up_player import *

import work_materials.globals
from libs.resorses import *

sys.path.append('../')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
#Подключение логгирования процессов
multiprocessing.log_to_stderr()
logger = multiprocessing.get_logger()
logger.setLevel(logging.INFO)

work_materials.globals.processing = 1


def move_player(bot, job):
    player = job.context.get('player')
    update_status('In Location', player, job.context.get('user_data'))
    update_location(job.context.get('location_id'), player, job.context.get('user_data'))
    print(player.nickname, "Переместился в новую локацию -", player.location)
    players_need_update.put(player)
    show_general_buttons(bot, job.context.get('update'), job.context.get('user_data'))


def add_resource(bot, update, args):
    item = Resourse(int(args[0]))
    player = get_player(update.message.from_user.id)
    print("code = ", player.add_item(player.res_backpack, item, int(args[1])))


def remove_resource(bot, update, args):
    item = Resourse(int(args[0]))
    player = get_player(update.message.from_user.id)
    print("code = ", player.remove_item(player.res_backpack, item, int(args[1])))
    
    
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
        bot.send_message(chat_id=update.message.chat_id, text="Вы отправились в локацию: {0}, до нее идти {1} минут".format(locations.get(new_loc_id).name, paths.get(new_loc_id)))
        #TODO запустить таймер и после него уже изменять локацию игрока и выводить новые кнопки
        contexts = {'chat_id': update.message.chat_id, 'location_id': new_loc_id, 'player': player,
                   'update': update, 'user_data': user_data}
        if filter_is_admin(update.message):
            bot.send_message(chat_id=update.message.chat_id, text="Вы можете использовать /fasttravel")
        user_data.update({'new_location': new_loc_id})
        travel_jobs.update({player.id: job.run_once(move_player, paths.get(new_loc_id) * 60, context=contexts)})
        return


def fast_travel(bot, update, user_data):
    bot.send_message(chat_id=update.message.chat_id, text="Fast Travel")
    player = get_player(update.message.from_user.id)
    travel_jobs.get(player.id).run(bot)


#Фильтр на старт игры
dispatcher.add_handler(CommandHandler("start", start, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_classes, class_select, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_fractions, fraction_select, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_sex_select, sex_select, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_nickname_select, nickname_select, pass_user_data=True))

#Команды для админов
dispatcher.add_handler(CommandHandler("setstatus", set_status, pass_user_data=True, filters = filter_is_admin, pass_args=True))
dispatcher.add_handler(CommandHandler("sql", sql, pass_user_data=True, filters = filter_is_admin))
dispatcher.add_handler(CommandHandler("delete_self", delete_self, pass_user_data=True, filters = filter_is_admin))
dispatcher.add_handler(CommandHandler("showdata", show_data, pass_user_data=True, filters=filter_is_admin))
dispatcher.add_handler(CommandHandler("fasttravel", fast_travel, pass_user_data=True, filters=filter_is_admin & fast_travel_filter))
dispatcher.add_handler(CommandHandler("return", return_to_location, pass_user_data=True, filters=filter_is_admin))

#Фильтр для вывода инфаормации об игроке
dispatcher.add_handler(CommandHandler("me", print_player, pass_user_data=True))

#Фильтры для повышения уровня игрока
dispatcher.add_handler(CommandHandler("lvl_up", choose_skill, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_lvl_up_skill, lvl_up_skill, pass_user_data=True))
dispatcher.add_handler(CommandHandler("lvl_up_points", choose_points, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and filter_lvl_up_points, lvl_up_points, pass_user_data=True))

#Фильтр для перемещения
dispatcher.add_handler(MessageHandler(Filters.text and location_filter and travel_filter, travel, pass_user_data=True))
dispatcher.add_handler(MessageHandler(Filters.text and choosing_way_filter, choose_way, pass_user_data=True))

#Команды для добавления и удаления предметов
dispatcher.add_handler(CommandHandler("add_resource", add_resource, pass_user_data=False, pass_args=True))
dispatcher.add_handler(CommandHandler("remove_resource", remove_resource, pass_user_data=False, pass_args=True))


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
