from bin.show_general_buttons import show_general_buttons
from work_materials.globals import *
from bin.player_service import update_status, update_location, get_player
from libs.myJob import MyJob
from work_materials.filters.service_filters import filter_is_admin


def move_player(bot, job):
    player = job.context.get('player')
    user_data = job.context.get('user_data')
    update_status('In Location', player, user_data)
    update_location(job.context.get('location_id'), player, user_data)
    print(player.nickname, "Переместился в новую локацию -", player.location)
    players_need_update.put(player)
    show_general_buttons(bot, job.context.get('update'), user_data)


def travel(bot, update, user_data):
    player = get_player(update.message.from_user.id)
    user_data.update({'location': player.location})
    user_data.update({'location_name': locations.get(player.location).name})
    current_location = locations.get(player.location)
    paths = current_location.roads
    path_buttons = []
    for i in paths:
        path_buttons.append(KeyboardButton(locations.get(i).name))
    path_buttons.append(KeyboardButton("Назад"))
    road_buttons = ReplyKeyboardMarkup(build_menu(path_buttons, n_cols=2), resize_keyboard=True, one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Вы в локации: {0}".format(current_location.name), reply_markup=road_buttons)
    update_status('Choosing way', player, user_data)


def choose_way(bot, update, user_data):
    if update.message.text == 'Назад':
        update_status('In Location', get_player(update.message.from_user.id), user_data)
        show_general_buttons(bot, update, user_data)
        return
    player = get_player(update.message.from_user.id)
    current_location = locations.get(player.location)
    paths = current_location.roads
    loc_name = update.message.text
    new_loc_id = 0
    for i in paths.keys():
        tmp_location = i
        if locations.get(tmp_location).name == loc_name:
            new_loc_id = tmp_location
            break
    if new_loc_id == 0:
        logging.error('ERROR: NO SUCH ID bot.py in choose_way, id = 0')
    else:
        update_status('Traveling', player, user_data)
        bot.send_message(chat_id=update.message.chat_id, text="Вы отправились в локацию: {0}, до нее идти {1} минут".format(locations.get(new_loc_id).name, paths.get(new_loc_id)), reply_markup=traveling_buttons)
        contexts = {'chat_id': update.message.chat_id, 'location_id': new_loc_id, 'player': player,
                   'update': update, 'user_data': user_data}
        if filter_is_admin(update.message):
            bot.send_message(chat_id=update.message.chat_id, text="Вы можете использовать /fasttravel")
        user_data.update({'new_location': new_loc_id})
        tmp_job = job.run_once(move_player, paths.get(new_loc_id) * 60, context=contexts)
        j = MyJob(tmp_job, paths.get(new_loc_id) * 60)
        travel_jobs.update({player.id: j})
        return


def fast_travel(bot, update, user_data):
    player = get_player(update.message.from_user.id)
    j = travel_jobs.get(player.id)
    print(j.get_time_left())
    if j is not None:
        j.job.schedule_removal()
        j.job.run(bot)

def return_to_location_admin(bot, update, user_data):
    player = get_player(update.message.from_user.id)
    update_status('In Location', player, user_data)
    update_location(player.location, player, user_data)
    j = travel_jobs.get(player.id)
    bot.send_message(chat_id=update.message.chat_id,text="Вы вернулись в локацию: {0}".format(locations.get(player.location).name))
    show_general_buttons(bot, update, user_data)
    if j is None:
        return
    j.job.schedule_removal()


def return_to_location(bot, update, user_data):
    player = get_player(update.message.from_user.id)
    j = travel_jobs.get(player.id)
    if j is None:
        bot.send_message(chat_id=update.message.chat_id, text="Вы стоите на месте, наверное вы заблудились /return")
        return
    j.job.schedule_removal()
    j.swap_time()
    new_loc_id = user_data.get('location')
    tmp_loc = user_data.get('location')
    user_data.update({'location': user_data.get('new_location')})
    user_data.update({'new_location': tmp_loc})
    sec = int(j.get_time_left()%60)
    time_str = '' + str(int(j.get_time_left()//60)) + ':' + ('0' if sec < 10 else '') + str(sec)
    location_name = locations.get(new_loc_id).name
    user_data.update({'location_name': location_name})
    contexts = {'chat_id': update.message.chat_id, 'location_id': new_loc_id, 'player': player,
                'update': update, 'user_data': user_data}
    bot.send_message(chat_id=update.message.chat_id, text="Вы решили вернуться в локацию {0}, осталось идти: <b>{1}</b>".format(
        location_name, time_str
    ), parse_mode='HTML')
    j.job = job.run_once(move_player, j.get_time_left(), context=contexts)