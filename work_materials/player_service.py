from work_materials.globals import *
from libs.player import *

def get_player(id):
    player = players.get(id)
    if player is not None:
        return player
    player = Player(id, 0, 0, 0, 0, 0, 0)
    if player.update_from_database(cursor) is None:
        return None
    players.update({player.id: player})
    return player


def update_location(location, player, user_data):
    player.location = location
    players.update({player.id: player})
    players_need_update.put(player)
    user_data.update({'location': location})
    user_data.update({'location_name': locations.get(location).name})


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


def set_status(bot, update, user_data, args):
    print('printing status')
    status = ''
    j = 0
    for i in args:
        status += i
        if j != len(args) - 1:
            status += ' '
        j += 1
    print(status)
    update_status(status, update.message.from_user.id, user_data)
    print(user_data)


def show_data(bot, update, user_data):
    print(user_data)
    msg = ''
    for i in user_data.keys():
        msg += str(i)
        msg += ' - '
        msg += str(user_data.get(i))
        msg += "\n"
    bot.send_message(chat_id=update.message.chat_id, text=msg)


def update_status(status, id, user_data):
    player = get_player(id)
    player.status = status
    players.update({id: player})
    user_data.update({"status": status})


def print_player(bot, update, user_data):
    id = update.message.from_user.id
    player = get_player(id)
    if player is None:
        return
    if player.sex == 0:
        sex = 'Мужской'
    else:
        sex = 'Женский'
    bot.send_message(chat_id=update.message.chat_id, text="Ник - <b>{0}</b>\nПол - <b>{1}</b>\nРаса - <b>{2}</b>\nФракция - <b>{3}</b>\nClass - <b>{4}</b>"
                                                          "\n\nStatus - <b>{5}</b>\n\nexp = <b>{6}</b>\nlvl = <b>{7}</b>\nFree_points = <b>{8}</b>"
                                                          "\nFree_skill_points = <b>{9}</b>\nFatigue = <b>{10}</b>\n\n"
                                                          "Первый навык - <b>{11}</b>-го уровня\nВторой навык - <b>{12}</b>-го уровня"
                                                          "\nТретий навык - <b>{13}</b>-го уровня\n"
                                                          "Четвертый навык - <b>{14}</b>-го уровня\n"
                                                          "Пятый навык - <b>{15}</b>-го уровня\n\nВыносливость - <b>{16}</b>\n"
                                                          "Броня - <b>{17}</b>\nСила - <b>{18}</b>\nЛовкость - <b>{19}</b>\n"
                                                          "Очки маны - <b>{20}</b>".format(
        player.nickname, sex, player.race, player.fraction,
        player.game_class, player.status, player.exp, player.lvl,
        player.free_points, player.free_skill_points, player.fatigue,
        player.first_skill_lvl, player.second_skill_lvl, player.third_skill_lvl,
        player.fourth_skill_lvl, player.fifth_skill_lvl, player.stats["endurance"],
        player.stats["armor"], player.stats["power"], player.stats["agility"], player.stats["mana_points"]),
        parse_mode="HTML")