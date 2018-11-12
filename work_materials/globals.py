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

dispatcher = updater.dispatcher

players = {}
players_need_update = Queue()

#Подключаем базу данных, выставляем кодировку
print("Enter password for database:")
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

locations = {1: portal, 2: human_castle, 3: elf_castle, 4: orc_castle, 5: human_south_tower, 6: human_north_tower, 7: elf_south_tower,
             8: elf_north_tower, 9: orcs_south_tower, 10: orcs_north_tower, 11: resources_btw_HE, 12: resources_btw_EO, 13: resources_btw_HO,
             14: human_capital, 15: elf_capital, 16: orc_capital, 17: human_guild_castle, 18: elf_guild_castle, 19: orc_guild_castle,
             20: human_forest, 21: human_mine, 22: elf_forest, 23: elf_mine, 24: orc_forest, 25: orc_mine, 26: human_farm_loc_010,
             27: human_farm_loc_1020, 28: human_farm_loc_2030, 29: human_farm_loc_3040, 30: human_farm_loc_4050, 31: elf_farm_loc_010,
             32: elf_farm_loc_1020, 33: elf_farm_loc_2030, 34: elf_farm_loc_3040, 35: elf_farm_loc_4050, 36: orc_farm_loc_010,
             37: orc_farm_loc_1020, 38: orc_farm_loc_2030, 39: orc_farm_loc_3040, 40: orc_farm_loc_4050}


def build_menu(buttons, n_cols, header_buttons = None, footer_buttons = None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


__capital_button_list = [
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
    KeyboardButton('Отправиться')
]
guild_buttons = ReplyKeyboardMarkup(build_menu(__guild_button_list, n_cols=2), resize_keyboard=True)

__location_button_list = [
    KeyboardButton('Исследовать'),  #фарм
    KeyboardButton('Отправиться')  #TODO Добавить еще кнопок
]
farmLocation_buttons = ReplyKeyboardMarkup(build_menu(__location_button_list, n_cols=2), resize_keyboard=True)

__resource_button_list = [
    KeyboardButton('Добывать'),  #фарм
    KeyboardButton('Отправиться')   #TODO Добавить еще кнопок
]
resource_buttons = ReplyKeyboardMarkup(build_menu(__resource_button_list, n_cols=2), resize_keyboard=True)

__resource2_button_list = [
    KeyboardButton('Добывать'),  #фарм
    KeyboardButton('Встать на атаку'),
    KeyboardButton('Отправиться')   #TODO Добавить еще кнопок
]
resource_buttons_offIsland = ReplyKeyboardMarkup(build_menu(__resource_button_list, n_cols=2), resize_keyboard=True)

__portal_button_list = [
    KeyboardButton('Войти в портал'),
    KeyboardButton('Встать на атаку'),
    KeyboardButton('Отправиться')
]
portal_buttons = ReplyKeyboardMarkup(build_menu(__portal_button_list, n_cols=2), resize_keyboard=True)

__castle_button_list = [
    KeyboardButton('Встать на атаку'),
    KeyboardButton('Отправиться')
]
castle_buttons = ReplyKeyboardMarkup(build_menu(__castle_button_list, n_cols=2), resize_keyboard=True)

__tower_button_list = [
    KeyboardButton('Встать на атаку'),
    KeyboardButton('Отправиться')
]
tower_buttons = ReplyKeyboardMarkup(build_menu(__tower_button_list, n_cols=2), resize_keyboard=True)

