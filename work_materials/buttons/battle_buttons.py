from telegram import KeyboardButton, ReplyKeyboardMarkup
from work_materials.globals import build_menu

def get_general_battle_buttons(player):
    __general_battle_buttons = [
        KeyboardButton('Атака ебать')
    ]
    n_cols = 3
    for i in range(0, 5):
        if player.skill_lvl[i] == 1:
            __general_battle_buttons.append(KeyboardButton(player.skill_name[i]))
            n_cols += 1
    __general_battle_buttons.append(KeyboardButton('Использовать предмет'))     #TODO Сделать использование предметов в сообщении по /use_
    __general_battle_buttons.append(KeyboardButton('Голосование ((флекс))'))
    __general_battle_buttons.append(KeyboardButton('Пропуск хода'))
    if n_cols % 2 == 0:
        n_cols = 2
    elif n_cols % 3 == 0:
        n_cols = 3
    elif n_cols == 5:
        n_cols = 2
    elif n_cols == 7:
        n_cols = 3
    else:
        n_cols = 2
    return ReplyKeyboardMarkup(build_menu(__general_battle_buttons, n_cols), resize_keyboard=True)


def get_enemies_buttons(battle, team):
    enemy_team_n = (team + 1) % 2
    __enemies_buttons = []
    enemy_team = battle.teams[enemy_team_n]
    for i in enemy_team:
        __enemies_buttons.append(KeyboardButton(i.participant.player.nickname))		#TODO Check
    __enemies_buttons.append(KeyboardButton('Отмена'))
