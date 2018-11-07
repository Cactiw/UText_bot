from telegram.ext import Updater
import MySQLdb, sys, logging

updater = Updater(token='757939309:AAE3QMqbT8oeyZ44es-l6eSzxpy1toCf_Bk')

dispatcher = updater.dispatcher

#Подключаем базу данных, выставляем кодировку
print("Enter password for database:")
passwd = input()
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