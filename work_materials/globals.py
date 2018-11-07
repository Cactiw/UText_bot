from telegram.ext import Updater
from telegram import KeyboardButton, ReplyKeyboardMarkup
import MySQLdb, sys, logging

updater = Updater(token='757939309:AAE3QMqbT8oeyZ44es-l6eSzxpy1toCf_Bk')

dispatcher = updater.dispatcher

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

admin_id_list = [231900398, 212657053]

processing = 1


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