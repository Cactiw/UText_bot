from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from work_materials.globals import build_menu, skill_names, dispatcher


def get_general_battle_buttons(player):
    if dispatcher.user_data.get(player.id).get('status') == "Battle_dead":
        return ReplyKeyboardRemove()
    __general_battle_buttons = []
    n_cols = 3
    all_skills = skill_names.get(player.game_class)
    for i in range(len(all_skills) - 1):
        if i == 0:
            __general_battle_buttons.append(KeyboardButton(all_skills[i]))
            n_cols += 1
            continue
        if player.skill_lvl[i - 1] > 0:
            __general_battle_buttons.append(KeyboardButton(all_skills[i]))
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
        __enemies_buttons.append(KeyboardButton(i.participant.nickname))
    __enemies_buttons.append(KeyboardButton('Отмена'))
    return ReplyKeyboardMarkup(build_menu(__enemies_buttons, 2), resize_keyboard=True)


def get_allies_buttons(battle, team):
    __ally_buttons = []
    ally_team = battle.teams[team]
    for i in ally_team:
        __ally_buttons.append(KeyboardButton(i.participant.nickname))
    __ally_buttons.append(KeyboardButton('Отмена'))
    return ReplyKeyboardMarkup(build_menu(__ally_buttons, 2), resize_keyboard=True)


def get_all_targets_buttons(battle, team):
    __all_buttons = []
    all_team = battle.teams[team]
    for i in all_team:
        __all_buttons.append(KeyboardButton(i.participant.nickname))
    __all_buttons.append(KeyboardButton('Отмена'))
    return ReplyKeyboardMarkup(build_menu(__all_buttons, 2), resize_keyboard=True)

__cancel =[
    KeyboardButton('Отмена')
]
cancel_button = ReplyKeyboardMarkup(build_menu(__cancel, 1), resize_keyboard=True)
