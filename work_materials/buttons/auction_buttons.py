from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from work_materials.globals import *

__auction_button_list = [
        InlineKeyboardButton("Оружие", callback_data="au ew"),
        InlineKeyboardButton("Голова", callback_data="au eh"),
        InlineKeyboardButton("Тело", callback_data="au eb"),
        InlineKeyboardButton("Перчатки", callback_data="au es"),
        InlineKeyboardButton("Ноги", callback_data="au ez"),
        InlineKeyboardButton("Средства передвижения", callback_data="au em"),
        InlineKeyboardButton("Импланты", callback_data="au ei"),
    ]

__auction_footer_buttons = [
        InlineKeyboardButton("Пойти нахуй", callback_data="au nahuy")
    ]
auction_reply_markup = InlineKeyboardMarkup(build_menu(__auction_button_list, n_cols=3, footer_buttons=__auction_footer_buttons))