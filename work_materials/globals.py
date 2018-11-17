from telegram.ext import Updater
from telegram import KeyboardButton, ReplyKeyboardMarkup
import MySQLdb, sys, logging
from multiprocessing import Process, Queue
from libs.locations.capital import *
from libs.locations.castle import *
from libs.locations.farm_location import *
from libs.locations.guild_castle import *
from libs.locations.portal import *
from libs.locations.resource_loc import *
from libs.locations.tower import *


updater = Updater(token='757939309:AAE3QMqbT8oeyZ44es-l6eSzxpy1toCf_Bk')
job = updater.job_queue

dispatcher = updater.dispatcher

players = {}
players_need_update = Queue()
travel_jobs = {}

#Подключаем базу данных, выставляем кодировку
#print("Enter password for database:")
passwd = 'fiP3Gahz'
conn = MySQLdb.connect('localhost', 'UText_bot', passwd, 'UText_bot')

cursor = conn.cursor()
conn.set_character_set('utf8')
# conn.set_character_set('utf8mb4')
# cursor.execute('SET NAMES utf8mb4;')
# cursor.execute('SET CHARACTER SET utf8mb4;')
# cursor.execute('SET character_set_connection=utf8mb4;')
print("Connection successful, starting bot")

admin_id_list = [231900398, 212657053, 307125511]

processing = 1

locations = {1: portal, 2: feds_castle, 3: trib_castle, 4: stai_castle, 5: feds_south_tower, 6: feds_north_tower, 7: trib_south_tower,
             8: trib_north_tower, 9: stai_south_tower, 10: stai_north_tower, 11: resources_btw_HE, 12: resources_btw_EO, 13: resources_btw_HO,
             14: feds_capital, 15: trib_capital, 16: stai_capital, 17: feds_guild_castle, 18: trib_guild_castle, 19: stai_guild_castle,
             20: feds_forest, 21: feds_mine, 22: trib_forest, 23: trib_mine, 24: stai_forest, 25: stai_mine, 26: feds_farm_loc_010,
             27: feds_farm_loc_1020, 28: feds_farm_loc_2030, 29: feds_farm_loc_3040, 30: feds_farm_loc_4050, 31: trib_farm_loc_010,
             32: trib_farm_loc_1020, 33: trib_farm_loc_2030, 34: trib_farm_loc_3040, 35: trib_farm_loc_4050, 36: stai_farm_loc_010,
             37: stai_farm_loc_1020, 38: stai_farm_loc_2030, 39: stai_farm_loc_3040, 40: stai_farm_loc_4050}


def build_menu(buttons, n_cols, header_buttons = None, footer_buttons = None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


__capital_button_list = [
    KeyboardButton('Инфо'),
    KeyboardButton('Доска объявлений'),
    KeyboardButton('Таверна'),
    KeyboardButton('Торговец'),
    KeyboardButton('Отправиться')
]
capital_buttons = ReplyKeyboardMarkup(build_menu(__capital_button_list, n_cols=2), resize_keyboard=True)

__guild_button_list = [
    KeyboardButton('Доска объявлений'),
    KeyboardButton('Кузнец'),
    KeyboardButton('Алхимическая станция'),
    KeyboardButton('Стол зачарования'),  #Может стоить объеденить в какую-нибудь кнопку, придумай название
    KeyboardButton('Инфо'),
    KeyboardButton('Отправиться')
]
guild_buttons = ReplyKeyboardMarkup(build_menu(__guild_button_list, n_cols=2), resize_keyboard=True)

__location_button_list = [
    KeyboardButton('Инфо'),
    KeyboardButton('Исследовать'),  #фарм
    KeyboardButton('Отправиться')  #TODO Добавить еще кнопок
]
farmLocation_buttons = ReplyKeyboardMarkup(build_menu(__location_button_list, n_cols=2), resize_keyboard=True)

__resource_button_list = [
    KeyboardButton('Инфо'),
    KeyboardButton('Добывать'),  #фарм
    KeyboardButton('Отправиться')   #TODO Добавить еще кнопок
]
resource_buttons = ReplyKeyboardMarkup(build_menu(__resource_button_list, n_cols=2), resize_keyboard=True)

__resource2_button_list = [

    KeyboardButton('Добывать'),  #фарм
    KeyboardButton('Встать на атаку'),
    KeyboardButton('Инфо'),
    KeyboardButton('Отправиться')   #TODO Добавить еще кнопок
]
resource_buttons_offIsland = ReplyKeyboardMarkup(build_menu(__resource_button_list, n_cols=2), resize_keyboard=True)

__portal_button_list = [
    KeyboardButton('Инфо'),
    KeyboardButton('Войти в портал'),
    KeyboardButton('Встать на атаку'),
    KeyboardButton('Отправиться')
]
portal_buttons = ReplyKeyboardMarkup(build_menu(__portal_button_list, n_cols=2), resize_keyboard=True)

__castle_button_list = [
    KeyboardButton('Инфо'),
    KeyboardButton('Встать на атаку'),
    KeyboardButton('Отправиться')
]
castle_buttons = ReplyKeyboardMarkup(build_menu(__castle_button_list, n_cols=2), resize_keyboard=True)
tower_buttons = ReplyKeyboardMarkup(build_menu(__castle_button_list, n_cols=2), resize_keyboard=True)

__traveling_buttons_list = [
    KeyboardButton('Инфо'),
    KeyboardButton('Вернуться')
]
traveling_buttons = ReplyKeyboardMarkup(build_menu(__traveling_buttons_list, n_cols=2), resize_keyboard=True)

__info_buttons_list = [
    KeyboardButton('Рюкзак'),
    KeyboardButton('Импланты'),
    KeyboardButton('Назад')
]
info_buttons = ReplyKeyboardMarkup(build_menu(__info_buttons_list, n_cols=2), resize_keyboard=True)

