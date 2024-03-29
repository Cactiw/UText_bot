from telegram import KeyboardButton, ReplyKeyboardMarkup
from work_materials.globals import build_menu

__merchant_buttons_list = [
    KeyboardButton('Оружие'),
    KeyboardButton('Голова'),
    KeyboardButton('Тело'),
    KeyboardButton('Перчатки'),
    KeyboardButton('Ноги'),
    KeyboardButton('Средства передвижения'),
    KeyboardButton('Импланты'),
    KeyboardButton('Продать'),
    KeyboardButton('Назад')
]

merchant_buttons = ReplyKeyboardMarkup(build_menu(__merchant_buttons_list, n_cols=3), resize_keyboard=True)
