from bot import players, players_need_update
from work_materials.globals import *
from libs.player import Player
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


def players_update(q):
    try:
        data = q.get()
        while data is not None:
            data.update_to_database(conn, cursor)
            data = q.get()
        return
    except KeyboardInterrupt:
        if q.empty:
            print("No users need to be updated, return")
            return
        print("Writing all updated users to database, wait...")
        while not q.empty():
            data = q.get()
            data.update_to_database(conn, cursor)
        print("All users are in database and updated")
        return


def get_player(id):
    player = players.get(id)
    if player is not None:
        return player
    player = Player(id, 0, 0, 0, 0, 0, 0)
    if player.update_from_database(cursor) is None:
        return None
    players.update({player.id : player})
    return player


def update_status(status, id, user_data):
    player = get_player(id)
    player.status = status
    players.update({id: player})
    user_data.update({"status": status})


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
                                                                  "Сила - <b>{2}</b>\nЛовкость - <b>{3}</b>\n"
                                                                  "Очки маны - <b>{4}</b>".format(
            player.stats.get("endurance"), player.stats.get("armor"),
            player.stats.get("power"), player.stats.get("agility"),
            player.stats.get("mana_points")),
                         parse_mode = "HTML", reply_markup = ReplyKeyboardRemove())
        players.update({id: player})
        players_need_update.put(player)
        update_status("Rest", id, user_data)
        return

    update_status("Lvl_up_points", id, user_data)
    button_list = [
        KeyboardButton("Выносливость"),
        KeyboardButton("Броня"),
        KeyboardButton("Сила"),
        KeyboardButton("Ловкость"),
        KeyboardButton("Очки маны"),
        KeyboardButton("Готово")
    ]
    buttons = ReplyKeyboardMarkup(build_menu(button_list, n_cols=2), resize_keyboard=True, one_time_keyboard=False)

    if free_points == 1:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Вы можете улучшить <b>1</b> характеристику\n\nВыберите характеристику, которую хотите улучшить\n"
                              "Выносливость - <b>{0}</b>\nБроня - <b>{1}</b>\n"
                              "Сила - <b>{2}</b>\nЛовкость - <b>{3}</b>\n"
                              "Очки маны - <b>{4}</b>".format(player.stats.get("endurance"), player.stats.get("armor"),
                                                       player.stats.get("power"), player.stats.get("agility"),
                                                       player.stats.get("mana_points")),
                         parse_mode='HTML', reply_markup=buttons)
    elif free_points >= 2 or free_points <= 4:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Вы можете улучшить <b>{5}</b> характеристики\n\nВыберите характеристику, которую хотите улучшить\n"
                              "Выносливость - <b>{0}</b>\nБроня - <b>{1}</b>\n"
                              "Сила - <b>{2}</b>\nЛовкость - <b>{3}</b>\n"
                              "Очки маны - <b>{4}</b>".format(player.stats.get("endurance"), player.stats.get("armor"),
                                                       player.stats.get("power"), player.stats.get("agility"),
                                                       player.stats.get("mana_points"), free_points),
                         parse_mode='HTML', reply_markup=buttons)
    elif free_points >= 5:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Вы можете улучшить <b>{5}</b> характеристик\n\nВыберите характеристику, которую хотите улучшить\n"
                              "Выносливость - <b>{0}</b>\nБроня - <b>{1}</b>\n"
                              "Сила - <b>{2}</b>\nЛовкость - <b>{3}</b>\n"
                              "Очки маны - <b>{4}</b>".format(player.stats.get("endurance"), player.stats.get("armor"),
                                                       player.stats.get("power"), player.stats.get("agility"),
                                                       player.stats.get("mana_points"), free_points),
                         parse_mode='HTML', reply_markup=buttons)
    players.update({id: player})
    players_need_update.put(player)


def lvl_up_points(bot, update, user_data):
    id = update.message.from_user.id
    player = get_player(id)
    if player is None:
        return
    if update.message.text == "Готово":
        update_status("Rest", id, user_data)
        return
    else:
        player.lvl_up_point(update.message.text)
        player.free_points -= 1
        players.update({id: player})
        players_need_update.put(player)
        if(update.message.text == "Очки маны"):
            bot.send_message(chat_id=update.message.chat_id,
                             text="Увеличины <b>{0}</b>".format(update.message.text),
                             parse_mode='HTML')
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text="Улучшена <b>{0}</b>".format(update.message.text),
                             parse_mode='HTML')
        choose_points(bot, update, user_data)


def choose_skill(bot, update, user_data): #Сюда игрок попадает при нажатии /lvl_up, ему предлагается выбрать скилл, который он хочет вкачать
    id = update.message.from_user.id
    player = get_player(id)
    if player is None:
        return
    free_skill = player.free_skill_points
    if(free_skill < 0) :
        player.free_skill_points = 0
        free_skill = 0
    if free_skill == 0:
        bot.send_message(chat_id = update.message.chat_id,
                         text = "У вас нет очков навыков\n\n"
                                 "Первый навык - {0}-го уровня\nВторой навык - {1}-го уровня\n"
                                 "Третий навык - {2}-го уровня\nЧетвертый навык - {3}-го уровня\n"
                                 "Пятый навык - {4}-го уровня".format( player.first_skill_lvl, player.second_skill_lvl,
                                                                        player.third_skill_lvl, player.fourth_skill_lvl,
                                                                        player.fifth_skill_lvl),
                         reply_markup = ReplyKeyboardRemove()
                         )
        #player.status = "Lvl_up_point"
        #user_data.update({"status": "Lvl_up_points"})
        update_status("Lvl_up_points", id, user_data)
        players.update({id: player})
        players_need_update.put(player)
        choose_points(bot, update, user_data)
        return

    update_status("Lvl_up_skill", id, user_data)
    button_list = [
        KeyboardButton("1"),
        KeyboardButton("2"),
        KeyboardButton("3"),
        KeyboardButton("4"),
        KeyboardButton("5"),
        KeyboardButton("Готово")
    ]
    buttons = ReplyKeyboardMarkup(build_menu(button_list, n_cols=2), resize_keyboard=True, one_time_keyboard = False)

    if free_skill == 1:
        bot.send_message(chat_id=update.message.chat_id,
                        text = "Вы можете улучшить <b>1</b> навык\n\nВыберите навык, который хотите улучшить\n\n"
                               "Первый навык - {0}-го уровня\nВторой навык - {1}-го уровня\n"
                               "Третий навык - {2}-го уровня\nЧетвертый навык - {3}-го уровня\n"
                               "Пятый навык - {4}-го уровня".format(player.first_skill_lvl, player.second_skill_lvl,
                                                                    player.third_skill_lvl, player.fourth_skill_lvl,
                                                                    player.fifth_skill_lvl),
                        parse_mode = 'HTML', reply_markup = buttons)
    elif free_skill >= 2 and free_skill <= 4:
        bot.send_message(chat_id=update.message.chat_id,
                        text="Вы можете улучшить <b>{0}</b> навыкa\n\nВыберите навык, который хотите улучшить\n\n"
                             "Первый навык - {1}-го уровня\nВторой навык - {2}-го уровня\n"
                             "Третий навык - {3}-го уровня\nЧетвертый навык - {4}-го уровня\n"
                             "Пятый навык - {5}-го уровня".format(free_skill, player.first_skill_lvl,
                                                                  player.second_skill_lvl, player.third_skill_lvl,
                                                                  player.fourth_skill_lvl, player.fifth_skill_lvl),
                        parse_mode='HTML', reply_markup = buttons)
    elif free_skill >= 5:
        bot.send_message(chat_id=update.message.chat_id,
                        text="Вы можете улучшить <b>{0}</b> навыков\n\nВыберите навык, который хотите улучшить\n\n"
                             "Первый навык - {1}-го уровня\nВторой навык - {2}-го уровня\n"
                             "Третий навык - {3}-го уровня\nЧетвертый навык - {4}-го уровня\n"
                             "Пятый навык - {5}-го уровня".format(free_skill, player.first_skill_lvl,
                                                                  player.second_skill_lvl, player.third_skill_lvl,
                                                                  player.fourth_skill_lvl, player.fifth_skill_lvl),
                        parse_mode='HTML', reply_markup = buttons)
    players.update({id: player})
    players_need_update.put(player)


def lvl_up_skill(bot, update, user_data):
    id = update.message.from_user.id
    player = get_player(id)
    if player is None:
        return
    if update.message.text == "Готово":
        update_status("Lvl_up_points", id, user_data)
        bot.send_message(chat_id = update.message.from_user.id, text = "", reply_markup = ReplyKeyboardRemove())
        choose_points(bot, update, user_data)
    else:
        player.lvl_up_skill(update.message.text)
        player.free_skill_points -= 1
        players.update({id : player})
        players_need_update.put(player)
        bot.send_message(chat_id = update.message.chat_id, text = "Улучшен <b>{0}</b> скилл".format(update.message.text), parse_mode = 'HTML')
        choose_skill(bot, update, user_data)