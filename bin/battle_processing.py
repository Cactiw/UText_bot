import work_materials.globals as globals
from work_materials.buttons.battle_buttons import get_allies_buttons, get_enemies_buttons, \
    get_all_targets_buttons, cancel_button, get_general_battle_buttons
import work_materials.globals as globals
from work_materials.globals import pending_battles, dispatcher, battles_need_treating, interprocess_queue, treated_battles, skill_names
import logging
from libs.interprocess_dictionaty import InterprocessDictionary
from telegram import ReplyKeyboardRemove
from bin.player_service import get_message_group
import pickle
import time


def get_battle(battle_id):
    return globals.pending_battles.get(battle_id)


def get_player_choosing_from_battle_via_nick(battle, player_nickname):
    for i in range(battle.team_players_count):
        if battle.teams[0][i].participant.nickname == player_nickname:
            return battle.teams[0][i]
        if battle.teams[1][i].participant.nickname == player_nickname:
            return battle.teams[1][i]


def get_player_choosing_from_battle_via_id(battle, player_id):
    for i in range(battle.team_players_count):
        if battle.teams[0][i].participant.id == player_id:
            return battle.teams[0][i]
        if battle.teams[1][i].participant.id == player_id:
            return battle.teams[1][i]


def battle_cancel_choosing(bot, update, user_data):
    battle = get_battle(user_data.get('Battle id'))
    player_choosing = get_player_choosing_from_battle_via_id(battle, update.message.from_user.id)
    player_choosing.skill = None
    player_choosing.target = None
    bot.send_message(chat_id=update.message.from_user.id, text="Вы отменили выбор",
                     reply_markup=get_general_battle_buttons(player_choosing.participant))
    user_data.update({'status': 'Battle'})
    if player_choosing in battle.skills_queue:
        battle.skills_queue.remove(player_choosing)


def choose_enemy_target(bot, update, user_data):
    user_data.update({'chosen skill': update.message.text})
    battle = get_battle(user_data.get('Battle id'))
    if add_chosen_skill(update, user_data) == -1:
        return
    bot.send_message(chat_id=update.message.chat_id, text="Выберите цель",
                     reply_markup=get_enemies_buttons(battle, user_data.get('Team')))


def choose_friendly_target(bot, update, user_data):
    user_data.update({'chosen skill': update.message.text})
    if add_chosen_skill(update, user_data) == -1:
        return
    bot.send_message(chat_id=update.message.chat_id, text="Выберите цель",
                     reply_markup=get_allies_buttons(get_battle(user_data.get('Battle id')), user_data.get('Team')))


def choose_any_target(bot, update, user_data):
    user_data.update({'chosen skill': update.message.text})
    if add_chosen_skill(update, user_data) == -1:
        return
    bot.send_message(chat_id=update.message.chat_id, text="Выберите цель",
                     reply_markup=get_all_targets_buttons(get_battle(user_data.get('Battle id')), user_data.get('Team')))


def add_chosen_skill(update, user_data):
    battle = get_battle(user_data.get('Battle id'))
    player_choosing = get_player_choosing_from_battle_via_id(battle, update.message.from_user.id)
    res = player_choosing.participant.skill_avaliable(update.message.text)
    text = ""
    if res == 1:
        player_choosing.skill = update.message.text
        user_data.update({'status': 'Choosing target'})
        return 1
    elif res == -1:
        text += "Такого навыка нет"
    elif res == -2:
        text += "Этот навык недоступен"
    elif res == -3:
        text += "Этот навык еще не готов"    #TODO окончание слова
    dispatcher.bot.send_message(chat_id=update.message.from_user.id, text= text)
    return -1


def set_target(bot, update, user_data):
    battle = get_battle(user_data.get('Battle id'))
    player_choosing = get_player_choosing_from_battle_via_id(battle, update.message.from_user.id)
    new_target_choosing = get_player_choosing_from_battle_via_nick(battle, update.message.text)
    if new_target_choosing is None:
        bot.send_message(chat_id=update.message.chat_id, text="Нет игрока с ником '{0}'!".format(update.message.text))
        return
    target = new_target_choosing.participant
    player_choosing.target = target
    user_data.update({'status': 'Battle waiting'})
    bot.sync_send_message(chat_id= update.message.chat_id, text="Вы выбрали цель, ждем других игроков",
                     reply_markup=cancel_button)        #TODO Сообщение должно быть до следующего сообщение о просчете битвы, sync
    battle.skills_queue.append(player_choosing)
    if battle.is_ready():
        battles_need_treating.put(battle)
        pending_battles.pop(battle.id)


def battle_skip_turn(bot, update, user_data):
    battle = get_battle(user_data.get('Battle id'))
    player_choosing = get_player_choosing_from_battle_via_id(battle, update.message.from_user.id)
    player_choosing.skill = update.message.text
    player_choosing.target = player_choosing.participant
    user_data.update({'status': 'Battle waiting'})
    bot.sync_send_message(chat_id=player_choosing.participant.id, text="Ждем других игроков",
                                reply_markup=cancel_button)     #TODO Сообщение должно быть до следующего сообщение о просчете битвы, sync
    battle.skills_queue.append(player_choosing)
    if battle.is_ready():
        battles_need_treating.put(battle)
        pending_battles.pop(battle.id)


def check_win(battle):
    team1_alive = 0
    team2_alive = 0
    for i in range(battle.team_players_count):
        if team1_alive > 0 and team2_alive > 0:
            return -1
        if battle.teams[0][i].participant.nickname not in battle.dead_list:
            team1_alive += 1
        if battle.teams[1][i].participant.nickname not in battle.dead_list:
            team2_alive += 1
    if team1_alive > 0 and team2_alive > 0:
        return -1
    if team1_alive == 0 and team2_alive == 0:
        return 2
    if team1_alive == 0 and team2_alive > 0:
        return 1
    if team2_alive == 0 and team1_alive > 0:
        return 0

#skill == 6 => пропуск хода


def kick_out_players():

    while globals.processing:
        curr_time = time.time()
        for j in list(pending_battles):
            i = pending_battles.get(j)
            if curr_time - i.last_count_time >= 30:
                for t in range(2):
                    for l in range(i.team_players_count):
                        player_choosing = i.teams[t][l]
                        if player_choosing.skill is None or player_choosing.target is None:
                            player_choosing.skill = "Пропуск хода"
                            player_choosing.target = player_choosing.participant
                            i.skills_queue.append(player_choosing)
                            dispatcher.user_data.get(player_choosing.participant.id).update({'status': 'Battle waiting'})
                            dispatcher.bot.send_message(chat_id=player_choosing.participant.id, text="Вы не выбрали действие и пропускаете ход")
                            if i.is_ready():
                                battles_need_treating.put(i)
                                pending_battles.pop(i.id)


def battle_count():     #Тут считается битва в которой все выбрали действие, отдельный процесс, Не забыть сделать так, чтобы выполнялось в таком порядке, в котором было выбрано
                                #Возможно стоит едитить сообщение и проставлять галки для тех, кто уже готов
    try:
        while True:
            battle = battles_need_treating.get()
            team_strings = ["Team 1:\n", "Team 2:\n"]
            result_strings = ["Team 1:\n", "Team 2:\n"]
            for i in battle.skills_queue:
                if i.participant.nickname in battle.dead_list:
                    print(i.participant.nickname + "is dead")
                    dispatcher.bot.send_message(chat_id=get_player_choosing_from_battle_via_nick(battle, i.participant.nickname).participant.id,
                                                text="Вы мертвы", reply_markup=ReplyKeyboardRemove())
                    continue
                i.participant.use_skill(i.skill, i.target)
                team_strings[i.team] += "<b>{0}</b> использовал <b>{1}</b> на <b>{2}</b>\n".format(i.participant.nickname, i.skill, i.target.nickname)
            team_strings[0] += '\n'
            battle.skills_queue.clear()
            for i in range(2):
                for j in range(battle.team_players_count):
                    player_choosing = battle.teams[i][j]
                    player = player_choosing.participant
                    result_strings[i] += "<b>{0}</b> - <b>{1}</b>    {2} hp, {3} charge\n".format(player.nickname,
                                                                                                               player.game_class,
                                                                                                               player.hp,
                                                                                                               player.charge)   #TODO написать красиво
                    skills = skill_names.get(player.game_class)
                    for t in range(len(player.skill_cooldown)):
                        if player.skill_cooldown[t] > 0:
                            result_strings[i] += "    {0} - {1} ходов\n".format(skills[t + 1], player.skill_cooldown[t])
                            player.skill_cooldown[t] -= 1
                    player_choosing.target = None
                    player_choosing.skill = None
                    reply_markup = get_general_battle_buttons(player)
                    if player.nickname in battle.dead_list:
                        reply_markup = None
                    message_group = get_message_group(player.id)
                    dispatcher.bot.group_send_message(message_group, chat_id=player.id,
                                                text=team_strings[0] + team_strings[1],
                                                parse_mode="HTML", reply_markup=reply_markup)
                    print("sent message in group, text =", team_strings[0] + team_strings[1], "group =", message_group)
            result_strings[0] += '\n'
            for i in range(2):
                for j in range(battle.team_players_count):
                    player_choosing = battle.teams[i][j]
                    player = player_choosing.participant
                    dict = {'status': 'Battle'}
                    if player.dead == 1:
                        dict.update({'status': 'Battle_dead'})
                    interprocess_dictionary = InterprocessDictionary(player.id, "user_data", dict)
                    interprocess_queue.put(interprocess_dictionary)
                    reply_markup = get_general_battle_buttons(player)
                    if player.nickname in battle.dead_list:
                        reply_markup = None
                    message_group = get_message_group(player.id)
                    dispatcher.bot.group_send_message(message_group, chat_id=player.id, text =result_strings[0] + result_strings[1] +
                                                                         "\n/info_Имя Игрока - информация об игроке",
                                                parse_mode="HTML", reply_markup=reply_markup)         #TODO Добавить баффы/дебаффы
                    message_group.shedule_removal()
                    print("sent message in group, text =", result_strings[0] + result_strings[1], "group =", message_group)

            for i in range(2):
                for j in range(battle.team_players_count):
                    player_choosing = battle.teams[i][j]
                    player = player_choosing.participant
                    if player.hp <= 0:
                        battle.dead_list.append(player.nickname)
                        player.dead = 1
                        player_choosing.skill = 6
                        player_choosing.target = player
                        dispatcher.bot.send_message(chat_id=player.id, text="Вы мертвы!", reply_markup=ReplyKeyboardRemove())
                        interprocess_dictionary = InterprocessDictionary(player.id, "user_data", {'status': 'Battle_dead'})
                        interprocess_queue.put(interprocess_dictionary)
            res = check_win(battle)
            if res != -1:
                if res < 2:
                    for i in range(2):
                        for j in range(battle.team_players_count):
                            player_choosing = battle.teams[i][j]
                            player = player_choosing.participant
                            #message_group = get_message_group(player.id)
                            dispatcher.bot.sync_send_message(chat_id=player.id, text="{0} команда победила!".format(
                                "Первая" if res == 0 else "Вторая"))
                            interprocess_dictionary = InterprocessDictionary(player.id, "battle status return", {})
                            interprocess_queue.put(interprocess_dictionary)
                elif res == 2:
                    for i in range(2):
                        for j in range(battle.team_players_count):
                            player_choosing = battle.teams[i][j]
                            player = player_choosing.participant
                            #message_group = get_message_group(player.id)
                            dispatcher.bot.sync_send_message(chat_id=player.id, text="Ничья!")
                            interprocess_dictionary = InterprocessDictionary(player.id, "battle status return", {})
                            interprocess_queue.put(interprocess_dictionary)


            else:
                for i in range(2):
                    for j in range(battle.team_players_count):
                        player_choosing = battle.teams[i][j]
                        player = player_choosing.participant
                        interprocess_dictionary = InterprocessDictionary(player.id, "user_data", {'Battle waiting update': 1})
                        interprocess_queue.put(interprocess_dictionary)
                battle.last_count_time = time.time()
                treated_battles.put(battle)
    except KeyboardInterrupt:
        return 0


def send_waiting_msg(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Мммм, что это? Race condiotion? (Напишите разрабам, пожалуйста)")


def send_message_dead(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Вы мертвы!")


def put_in_pending_battles_from_queue():
    battle = treated_battles.get()
    while battle is not None:
        pending_battles.update({battle.id: battle})
        for i in range(2):
            for j in range(battle.team_players_count):
                player_choosing = battle.teams[i][j]
                player = player_choosing.participant
                interprocess_dictionary = InterprocessDictionary(player.id, "user_data", {'Battle waiting update': 0})
                interprocess_queue.put(interprocess_dictionary)
        battle = treated_battles.get()
    save_battles()


def save_battles():
    f = open('backup/battles', 'wb+')
    pickle.dump(pending_battles, f)
    f.close()
    logging.info("Battles has been written")
