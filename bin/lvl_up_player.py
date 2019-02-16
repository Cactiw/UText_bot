from telegram import ReplyKeyboardRemove
from bin.player_service import players, players_need_update, update_status, get_player
from bin.starting_player import start
from telegram import KeyboardButton, ReplyKeyboardMarkup
from work_materials.globals import build_menu, skills
from bin.show_general_buttons import show_general_buttons


def choose_points(bot, update, user_data):
    id = update.message.from_user.id
    player = get_player(id)
    if(player is None):
        return
    free_points = player.free_points
    if(free_points < 0):
        player.free_points = 0
        free_points = 0
    if(free_points == 0):
        bot.send_message(chat_id = update.message.chat_id, text = "У вас нет свободных очков\n\n"
                                                                  "Выносливость - <b>{0}</b>\nБроня - <b>{1}</b>\n"
                                                                  "Сила - <b>{2}</b>\nСкорость - <b>{3}</b>\n"
                                                                  "Заряд - <b>{4}</b>".format(
            player.stats.get("endurance"), player.stats.get("armor"),
            player.stats.get("power"), player.stats.get("speed"),
            player.stats.get("charge")),
                         parse_mode = "HTML", reply_markup = ReplyKeyboardRemove())
        players.update({id: player})
        players_need_update.put(player)
        update_status(user_data.get('saved_lvl_up_status'), player, user_data)
        user_data.pop('saved_lvl_up_status')
        show_general_buttons(bot, update, user_data)
        return

    update_status("Lvl_up_points", player, user_data)
    button_list = [
        KeyboardButton("Выносливость"),
        KeyboardButton("Броня"),
        KeyboardButton("Сила"),
        KeyboardButton("Скорость"),
        KeyboardButton("Заряд"),
        KeyboardButton("Готово")
    ]
    buttons = ReplyKeyboardMarkup(build_menu(button_list, n_cols=2), resize_keyboard=True, one_time_keyboard=False)
    s = ''
    if free_points == 1:
        s = "характеристику"
    elif free_points >= 2 or free_points <= 4:
        s = "характеристики"
    elif free_points >= 5:
        s = "характеристик"
    bot.send_message(chat_id=update.message.chat_id,
                     text="Вы можете улучшить <b>{5}</b> {6}\n\nВыберите характеристику, которую хотите улучшить\n"
                          "Выносливость - <b>{0}</b>\nБроня - <b>{1}</b>\n"
                          "Сила - <b>{2}</b>\nСкорость - <b>{3}</b>\n"
                          "Заряд- <b>{4}</b>".format(player.stats.get("endurance"), player.stats.get("armor"),
                                                     player.stats.get("power"), player.stats.get("speed"),
                                                     player.stats.get("charge"), free_points, s),
                     parse_mode='HTML', reply_markup=buttons)
    players.update({id: player})
    players_need_update.put(player)


def lvl_up_points(bot, update, user_data):
    id = update.message.from_user.id
    player = get_player(id)
    if player is None:
        return
    if update.message.text == "Готово":
        update_status(user_data.get('saved_lvl_up_status'), player, user_data)
        user_data.pop('saved_lvl_up_status')
        show_general_buttons(bot, update, user_data)
        return
    else:
        player.lvl_up_point(update.message.text)
        player.free_points -= 1
        players.update({id: player})
        players_need_update.put(player)
        if(update.message.text == "заряд"):
            bot.send_message(chat_id=update.message.chat_id,
                             text="Увеличины <b>{0}</b>".format(update.message.text),
                             parse_mode='HTML')
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text="Улучшена <b>{0}</b>".format(update.message.text),
                             parse_mode='HTML')
        choose_points(bot, update, user_data)


def lvl_up(bot, update, user_data):  # Сюда игрок попадает при нажатии /lvl_up, ему предлагается выбрать скилл
    id = update.message.from_user.id
    player = get_player(id)
    if player is None:
        start(bot, update, user_data)
        return
    user_data.update({'saved_lvl_up_status': user_data.get('status')})
    choose_skill(bot, update, user_data)


def choose_skill(bot, update, user_data):
    id = update.message.from_user.id
    player = get_player(id)
    if player is None:
        return
    free_skill = player.free_skill_points
    if free_skill < 0:
        player.free_skill_points = 0
        free_skill = 0
    if free_skill == 0:
        button_list = [
            KeyboardButton("Выносливость"),
            KeyboardButton("Броня"),
            KeyboardButton("Сила"),
            KeyboardButton("Скорость"),
            KeyboardButton("Заряд"),
            KeyboardButton("Готово")
        ]
        buttons = ReplyKeyboardMarkup(build_menu(button_list, n_cols=2), resize_keyboard=True, one_time_keyboard=False)
        bot.send_message(chat_id = update.message.chat_id,
                         text = "У вас нет очков навыков\n\n"
                                 "{5} - {0}-го уровня\n{6} - {1}-го уровня\n"
                                 "{7} - {2}-го уровня\n{8} - {3}-го уровня\n"
                                 "{9} - {4}-го уровня".format(list(player.skill_lvl.values())[0], list(player.skill_lvl.values())[1],
                                                              list(player.skill_lvl.values())[2], list(player.skill_lvl.values())[3],
                                                              list(player.skill_lvl.values())[4], list(player.skill_lvl)[0],
                                                              list(player.skill_lvl)[1], list(player.skill_lvl)[2],
                                                              list(player.skill_lvl)[3], list(player.skill_lvl)[4]),
                         reply_markup = buttons)
        update_status("Lvl_up_points", player, user_data)
        players.update({id: player})
        players_need_update.put(player)
        choose_points(bot, update, user_data)
        show_general_buttons(bot, update, user_data)
        return

    update_status("Lvl_up_skill", player, user_data)
    button_list = [
        KeyboardButton("1"),
        KeyboardButton("2"),
        KeyboardButton("3"),
        KeyboardButton("4"),
        KeyboardButton("5"),
        KeyboardButton("Готово")
    ]
    buttons = ReplyKeyboardMarkup(build_menu(button_list, n_cols=2), resize_keyboard=True, one_time_keyboard = False)
    s = ''
    if free_skill == 1:
        s = "навык"
    elif free_skill >= 2 and free_skill <= 4:
        s = "навыка"
    elif free_skill >= 5:
        s = "навыков"
    bot.send_message(chat_id=update.message.chat_id,
                     text="Вы можете улучшить <b>{5}</b> {6}\n\nВыберите навык, который хотите улучшить\n\n"
                          "{7} - {0}-го уровня\n{8} - {1}-го уровня\n"
                          "{9} - {2}-го уровня\n{10} - {3}-го уровня\n"
                          "{11} - {4}-го уровня".format(list(player.skill_lvl.values())[0], list(player.skill_lvl.values())[1], list(player.skill_lvl.values())[2],
                                                        list(player.skill_lvl.values())[3], list(player.skill_lvl.values())[4],  free_skill, s,
                                                        list(player.skill_lvl)[0], list(player.skill_lvl)[1], list(player.skill_lvl)[2], list(player.skill_lvl)[3], list(player.skill_lvl)[4]),
                     parse_mode='HTML', reply_markup=buttons)
    players.update({id: player})
    players_need_update.put(player)


def lvl_up_skill(bot, update, user_data):
    id = update.message.from_user.id
    player = get_player(id)
    if player is None:
        return
    if update.message.text == "Готово":
        update_status("Lvl_up_points", player, user_data)
        bot.send_message(chat_id = update.message.from_user.id, text="Теперь выберите очки характеристик")
        choose_points(bot, update, user_data)
    else:
        player.lvl_up_skill(update.message.text)
        player.free_skill_points -= 1
        players.update({id : player})
        players_need_update.put(player)
        bot.send_message(chat_id = update.message.chat_id, text="Улучшен <b>{0}</b> скилл".format(update.message.text), parse_mode='HTML')
        choose_skill(bot, update, user_data)
