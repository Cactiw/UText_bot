from vk_bot import KeyboardButton, ReplyKeyboardMarkup
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

__merchant_buttons_list = [
    KeyboardButton('Назад')
]

merchant_buy_buttons = ReplyKeyboardMarkup(build_menu(__merchant_buttons_list, n_cols=2), resize_keyboard=True)