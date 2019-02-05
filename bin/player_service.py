from work_materials.globals import *
from libs.player import *
from bin.equipment_service import *
from work_materials.filters.service_filters import filter_is_admin
import work_materials.globals as globals
from libs.message_group import message_groups, MessageGroup


def get_player(id, notify_not_found = True):
    player = players.get(id)
    if player is not None:
        update_location(player.location, player, dispatcher.user_data[id])
        return player
    player = Player(id, 0, 0, 0, 0, 0, 0)
    if player.update_from_database() is None:
        if notify_not_found:
            dispatcher.bot.send_message(chat_id=id, text = "Вы не зарегистрированы в игре. Нажмите /start")
        return None
    update_location(player.location, player, dispatcher.user_data[id])
    players.update({player.id: player})
    return player

def get_message_group(player_id):
    user_data = dispatcher.user_data.get(player_id)
    id = user_data.get("message_group")
    if id is None:
        group = MessageGroup(player_id)
        user_data.update({"message_group" : group.id})
    else:
        group = message_groups.get(id)
    if group is None or group.created_id != player_id:   #   Запись в user data устарела, группа уже не существует
        user_data.pop("message_group")
        return get_message_group(player_id)
    return group


def update_location(location, player, user_data):
    player.location = location
    players.update({player.id: player})
    players_need_update.put(player)
    user_data.update({'location': location})
    user_data.update({'location_name': locations.get(location).name})


def players_update(q):
    reconnect_database()
    globals.conn = psycopg2.connect("dbname=UText_bot user=UText_bot password={0}".format(passwd))

    globals.cursor = globals.conn.cursor()
    try:
        data = q.get()
        while data is not None:
            data.update_to_database()
            data = q.get()
        return
    except KeyboardInterrupt:
        if q.empty:
            print("No users need to be updated, return")
            return
        print("Writing all updated users to database, wait...")
        while not q.empty():
            data = q.get()
            data.update_to_database()
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
    if player.status != 'Info' and player.status != user_data.get('saved_info_status'):
        user_data.update({'saved_info_status': player.status})
    update_status('Info', player, user_data)
    if player.sex == 0:
        sex = 'Мужской'
    else:
        sex = 'Женский'
    task = ''
    if user_data.get('saved_info_status') == 'In Location':
        task += 'Отдых'
    elif user_data.get('saved_info_status') == 'Choosing way':
        task += 'Выбираете путь'
    elif user_data.get('saved_info_status') == 'Traveling':
        j = travel_jobs.get(player.id)
        if j is not None:
            time = j.get_time_left()
            time_str = '<b>'
            time_str += str(int(time//60))
            time_str += ':'
            sec = int(time%60)
            if sec < 10:
                time_str += '0'
            time_str += str(sec)
            time_str += '</b>'
            task += 'Перемещается в локацию: {0}, осталось: {1}'.format(locations.get(user_data.get('new_location')).name, time_str)
        else:
            task += "Вы стоите на месте, наверное вы заблудились, вернитесь"
            if filter_is_admin.filter(update.message):
                task += " /return"
    lvl_up_str = "У вас остались нераспределенные очки /lvl_up\n" if (player.free_points != 0 or player.free_skill_points != 0) else ""
    bot.send_message(chat_id=update.message.chat_id, text="Ник - <b>{0}</b>\nПол - <b>{1}</b>\nРаса - <b>{2}</b>\nФракция - <b>{3}</b>\nСейчас вы в локации: {21}\n\nКласс - <b>{4}</b>"
                                                          "\nКредиты - <b>{23}</b>\nМеханизмы - <b>{24}</b>\nМетаполимены - <b>{25}</b>"
                                                          "\n\nexp = <b>{5}</b>\nlvl = <b>{6}</b>\nFree_points = <b>{7}</b>"
                                                          "\nFree_skill_points = <b>{8}</b>\nFatigue = <b>{9}</b>\n{22}\n"
                                                          "Первый навык - <b>{10}</b>-го уровня\nВторой навык - <b>{11}</b>-го уровня"
                                                          "\nТретий навык - <b>{12}</b>-го уровня\n"
                                                          "Четвертый навык - <b>{13}</b>-го уровня\n"
                                                          "Пятый навык - <b>{14}</b>-го уровня\n\nВыносливость - <b>{15}</b>\n"
                                                          "Броня - <b>{16}</b>\nСила - <b>{17}</b>\nСкорость - <b>{18}</b>\n"
                                                          "Заряд - <b>{19}</b>\n\nЗанятие: {20}\n".format(
        player.nickname, sex, player.race, player.fraction,
        player.game_class, player.exp, player.lvl,
        player.free_points, player.free_skill_points, player.fatigue,
        list(player.skill_lvl.values())[1], list(player.skill_lvl.values())[2], list(player.skill_lvl.values())[3],
        list(player.skill_lvl.values())[4], list(player.skill_lvl.values())[5], player.stats["endurance"],
        player.stats["armor"], player.stats["power"], player.stats["speed"], player.stats["charge"], task,
        locations.get(player.location).name, lvl_up_str, player.resources.get('gold'), player.resources.get('wood'), player.resources.get('metal')),  #25
        parse_mode="HTML", reply_markup=info_buttons)
    
    
def show_equipment(bot, update):
    player = get_player(update.message.from_user.id)
    if player.on_character['head'] is not None:
        on_head = "<b>" + get_equipment(player.on_character['head']).name + "</b>   /unequip_head"
    else:
        on_head = 'Ничего'
    if player.on_character['body'] is not None:
        on_body = "<b>" + get_equipment(player.on_character['body']).name + "</b>   /unequip_body"
    else:
        on_body = 'Ничего'
    if player.on_character['shoulders'] is not None:
        on_shoulders = "<b>" + get_equipment(player.on_character['shoulders']).name + "</b>   /unequip_shoulders"
    else:
        on_shoulders = 'Ничего'
    if player.on_character['legs'] is not None:
        on_legs = "<b>" + get_equipment(player.on_character['legs']).name + "</b>   /unequip_legs"
    else:
        on_legs = 'Ничего'
    if player.on_character['feet'] is not None:
        on_feet = "<b>" + get_equipment(player.on_character['feet']).name + "</b>   /unequip_feet"
    else:
        on_feet = 'Ничего'
    if player.on_character['left_arm'] is not None:
        on_larm = "<b>" + get_equipment(player.on_character['left_arm']).name + "</b>   /unequip_left_arm"
    else:
        on_larm = 'Ничего'
    if player.on_character['right_arm'] is not None:
        on_rarm = "<b>" + get_equipment(player.on_character['right_arm']).name + "</b>   /unequip_right_arm"
    else:
        on_rarm = 'Ничего'
    if player.on_character['mount'] is not None:
        mount = "<b>" + get_equipment(player.on_character['mount']).name + "</b>   /unequip_mount"
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
        eq = get_equipment(i)
        print(eq.name)
        text += '<b>' + eq.name
        text += '</b>\n     '
        for j in eq.stats:
            stat = eq.stats.get(j)
            if stat != 0:
                text += j
                text += ' - <b>'
                text += str(stat)
                text += '</b>  '
        text += "\nАктивировать: /equip_{0}".format(i)
        text += "\nВыставить на аукцион: /create_lot_{0}_[начальная цена]_[цена выкупа]_[время в часах]".format(i)
        text += '\n\n'
    text += '\n\n<em>Расходуемые:</em>\n'
    text += '\n\n<em>Ресурсы:</em>\n'
    bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode = 'HTML')