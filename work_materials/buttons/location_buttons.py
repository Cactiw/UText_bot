from telegram import KeyboardButton, ReplyKeyboardMarkup
from work_materials.globals import build_menu

__capital_button_list = [
    KeyboardButton('Инфо'),
    KeyboardButton('Доска объявлений'),
    KeyboardButton('Аукцион'),
    KeyboardButton('Торговец'),
    KeyboardButton('Таверна'),
    KeyboardButton('Битва'),
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