from bin.show_general_buttons import show_general_buttons
from work_materials.globals import *
from libs.player import *
from bin.equipment_service import *


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
    update_status(status, get_player(update.message.from_user.id), user_data)
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


def update_status(status, player, user_data):
    player.status = status
    players.update({player.id: player})
    user_data.update({"status": status})


def print_player(bot, update, user_data):
    id = update.message.from_user.id
    player = get_player(id)
    if player is None:
        return
    if player.status != user_data.get('saved_status'):
        user_data.update({'saved_status': player.status})
    update_status('Info', player, user_data)
    if player.sex == 0:
        sex = 'Мужской'
    else:
        sex = 'Женский'
    task = ''
    if player.status == 'In Location':
        task += 'Отдых'
    elif player.status == 'Choosing way':
        task += 'Выбираете путь'
    elif player.status == 'Traveling':
        j = travel_jobs.get(player.id)
        #print(j.next_t)
        print(j)
        print(j.interval_seconds)
        time = j.interval
        print(time)
        task += 'Перемещается в локацию: {0}, осталось: {1}'.format(locations.get(user_data.get('new_location')).name, time)
    button_list = [
        KeyboardButton('Рюкзак'),
        KeyboardButton('Назад')
    ]
    buttons = ReplyKeyboardMarkup(build_menu(button_list, n_cols=2), resize_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Ник - <b>{0}</b>\nПол - <b>{1}</b>\nРаса - <b>{2}</b>\nФракция - <b>{3}</b>\nСейчас вы в локации: {22}\n\nКласс - <b>{4}</b>"
                                                          "\n\nСтатус - <b>{5}</b>\n\nexp = <b>{6}</b>\nlvl = <b>{7}</b>\nFree_points = <b>{8}</b>"
                                                          "\nFree_skill_points = <b>{9}</b>\nFatigue = <b>{10}</b>\n\n"
                                                          "Первый навык - <b>{11}</b>-го уровня\nВторой навык - <b>{12}</b>-го уровня"
                                                          "\nТретий навык - <b>{13}</b>-го уровня\n"
                                                          "Четвертый навык - <b>{14}</b>-го уровня\n"
                                                          "Пятый навык - <b>{15}</b>-го уровня\n\nВыносливость - <b>{16}</b>\n"
                                                          "Броня - <b>{17}</b>\nСила - <b>{18}</b>\nЛовкость - <b>{19}</b>\n"
                                                          "Очки маны - <b>{20}</b>\n\nЗанятие: {21}".format(
        player.nickname, sex, player.race, player.fraction,
        player.game_class, player.status, player.exp, player.lvl,
        player.free_points, player.free_skill_points, player.fatigue,
        player.first_skill_lvl, player.second_skill_lvl, player.third_skill_lvl,
        player.fourth_skill_lvl, player.fifth_skill_lvl, player.stats["endurance"],
        player.stats["armor"], player.stats["power"], player.stats["agility"], player.stats["mana_points"], task, locations.get(player.location).name),
        parse_mode="HTML", reply_markup=buttons)


def return_to_location(bot, update, user_data):
    player = get_player(update.message.from_user.id)
    update_status('In Location', player, user_data)
    update_location(player.location, player, user_data)
    j = travel_jobs.get(player.id)
    bot.send_message(chat_id=update.message.chat_id,text="Вы вернулись в локацию: {0}".format(locations.get(player.location).name))
    show_general_buttons(bot, update, user_data)
    if j is None:
        return
    j.schedule_removal()
    
    
def show_equipment(bot, update):
    player = get_player(update.message.from_user.id)
    #print(player.on_character['head'])
    #print(player.on_character['body'])
    if player.on_character['head'] is not None:
        on_head = "<b>" + get_equipment(player.on_character['head']).name + "</b>\nunequip: /unequip_head"
    else:
        on_head = 'Ничего'
    if player.on_character['body'] is not None:
        on_body = "<b>" + get_equipment(player.on_character['body']).name + "</b>\nunequip: /unequip_body"
    else:
        on_body = 'Ничего'
    if player.on_character['shoulders'] is not None:
        on_shoulders = "<b>" + get_equipment(player.on_character['shoulders']).name + "</b>\nunequip: /unequip_shoulders"
    else:
        on_shoulders = 'Ничего'
    if player.on_character['legs'] is not None:
        on_legs = "<b>" + get_equipment(player.on_character['legs']).name + "</b>\nunequip: /unequip_legs"
    else:
        on_legs = 'Ничего'
    if player.on_character['feet'] is not None:
        on_feet = "<b>" + get_equipment(player.on_character['feet']).name + "</b>\nunequip: /unequip_feet"
    else:
        on_feet = 'Ничего'
    if player.on_character['left_arm'] is not None:
        on_larm = "<b>" + get_equipment(player.on_character['left_arm']).name + "</b>\nunequip: /unequip_left_arm"
    else:
        on_larm = 'Ничего'
    if player.on_character['right_arm'] is not None:
        on_rarm = "<b>" + get_equipment(player.on_character['right_arm']).name + "</b>\nunequip: /unequip_right_arm"
    else:
        on_rarm = 'Ничего'
    if player.on_character['mount'] is not None:
        mount = "<b>" + get_equipment(player.on_character['mount']).name + "</b>\nunequip: /unequip_mount"
    else:
        mount = 'Ничего'
    bot.send_message(chat_id=update.message.chat_id, text="Голова - {0}\nТело - {1}\nПлечи - {2}\nНоги - {3}\n"
                                                              "Ботинки - {4}\nЛевая рука - {5}\n"
                                                              "Правая рука - {6}\nСредство передвижения - {7}".format(on_head, on_body,
                                                            on_shoulders, on_legs, on_feet, on_larm, on_rarm, mount), parse_mode = 'HTML')


def print_backpacks(bot, update, user_data):
    player = get_player(update.message.from_user.id)
    text = '<em>Экипировка:</em>\n'
    for i in player.eq_backpack:
        #print(i)
        #print(player.eq_backpack.get(i))
        eq = get_equipment(i)
        text += '<b>' + eq.name
        text += '</b>\n     '
        for j in eq.stats:
            stat = eq.stats.get(j)
            if stat != 0:
                text += j
                text += ' - <b>'
                text += str(stat)
                text += '</b>  '
        text += "\nequip: /equip_{0}".format(i)
        text += '\n\n'
    text += '\n\n<em>Расходуемые:</em>\n'
    text += '\n\n<em>Ресурсы:</em>\n'
    bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode = 'HTML')