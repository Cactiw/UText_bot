from telegram import KeyboardButton, ReplyKeyboardMarkup
from work_materials.globals import build_menu


__farming_buttons = [
    KeyboardButton("Вернуться в локацию"),
]

farming_buttons = ReplyKeyboardMarkup(build_menu(__farming_buttons, n_cols=2), resize_keyboard=True)
