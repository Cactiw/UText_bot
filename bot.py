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

from bin.service_commands import *
from bin.starting_player import *
from bin.save_load_user_data import *
from bin.show_general_buttons import show_general_buttons
from bin.lvl_up_player import *

import work_materials.globals
from libs.resorses import *

sys.path.append('../')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
#Подключение логгирования процессов
multiprocessing.log_to_stderr()
logger = multiprocessing.get_logger()
logger.setLevel(logging.INFO)



work_materials.globals.processing = 1


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


def set_status(bot, update, user_data, args):
    print('printing status')
    status = ''
    j = 0
    for i in args:
        status += i
        if j != len(args) - 1:
            status += ' '
        j += 1
    print(status)
    update_status(status, update.message.from_user.id, user_data)
    print(user_data)


def show_data(bot, update, user_data):
    print(user_data)
    msg = ''
    for i in user_data.keys():
        msg += str(i)
        msg += ' - '
        msg += str(user_data.get(i))
        msg += "\n"
    bot.send_message(chat_id=update.message.chat_id, text=msg)


def update_status(status, id, user_data):
    player = get_player(id)
    player.status = status
    players.update({id: player})
    user_data.update({"status": status})


def update_location(location, id, user_data):
    player = get_player(id)
    player.location = location
    players.update({id: player})
    user_data.update({"location": location})


def get_player(id):
    player = players.get(id)
    if player is not None:
        return player
    player = Player(id, 0, 0, 0, 0, 0, 0)
    if player.update_from_database(cursor) is None:
        return None
    players.update({player.id : player})
    return player


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


def add_resource(bot, update, args):
    item = Resourse(int(args[0]))
    player = get_player(update.message.from_user.id)
    print("code = ", player.add_item(player.res_backpack, item, int(args[1])))


def remove_resource(bot, update, args):
    item = Resourse(int(args[0]))
    player = get_player(update.message.from_user.id)
    print("code = ", player.remove_item(player.res_backpack, item, int(args[1])))
    
    
def travel(bot, update, user_data):
    print("in travel")
    print(update.message.text)
    player = get_player(update.message.from_user.id)
    current_location = locations.get(player.location)
    paths = current_location.roads
    path_buttons = []
    for i in paths:
        path_buttons.append(KeyboardButton(locations.get(i).name))
    path_buttons.append(KeyboardButton("Назад"))
    road_buttons = ReplyKeyboardMarkup(build_menu(path_buttons, n_cols=2), resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Вы в локации: {0}".format(current_location.name), reply_markup=road_buttons)
    update_status('Choosing way', player.id, user_data)
    print(user_data)


def choose_way(bot, update, user_data):
    print("in choose way")
    print(user_data)
    if update.message.text == 'Назад':
        update_status('In Location', update.message.from_user.id, user_data)
        show_general_buttons(bot, update, user_data)
        return
    player = get_player(update.message.from_user.id)
    current_location = locations.get(player.location)
    paths = current_location.roads
    print(paths)
    loc_name = update.message.text
    print(loc_name)
    new_loc_id = 0
    for i in paths.keys():
        tmp_location = i
        print(tmp_location, " - ", locations.get(tmp_location).name)
        if locations.get(tmp_location).name == loc_name:
            new_loc_id = tmp_location
            print("new_loc = ", new_loc_id)
            break
    if new_loc_id == 0:
        work_materials.globals.logging.error('ERROR: NO SUCH ID bot.py in choose_way, id = 0')
    else:
        update_status('Traveling', player.id, user_data)
        bot.send_message(chat_id=update.message.chat_id, text="Вы отправились в локацию: {0}".format(locations.get(new_loc_id).name))
        #TODO запустить таймер и после него уже изменять локацию игрока и выводить новые кнопки
        update_status('In Location', player.id, user_data)
        update_location(new_loc_id, player.id, user_data)
        print("Переместился в новую локацию - ", player.location)
        players_need_update.put(player)
        show_general_buttons(bot, update, user_data)


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
