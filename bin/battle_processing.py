from work_materials.buttons.battle_buttons import get_allies_buttons, get_enemies_buttons, \
    get_all_targets_buttons, cancel_button, get_general_battle_buttons
from work_materials.globals import pending_battles, dispatcher, battles_need_treating, interprocess_queue, treated_battles, skill_names
import logging
from libs.interprocess_dictionaty import InterprocessDictionary
from bin.show_general_buttons import show_general_buttons


def get_battle(battle_id):
    return pending_battles.get(battle_id)


def get_player_choosing_from_battle_via_nick(battle, player_nickname):
    for i in range(battle.team_players_count):
        if battle.teams[0][i].participant.nickname == player_nickname:
            return battle.teams[0][i]
        if battle.teams[1][i].participant.nickname == player_nickname:
            return battle.teams[1][i]
    logging.error("No such player in battle\n")


def get_player_choosing_from_battle_via_id(battle, player_id):
    for i in range(battle.team_players_count):
        if battle.teams[0][i].participant.id == player_id:
            return battle.teams[0][i]
        if battle.teams[1][i].participant.id == player_id:
            return battle.teams[1][i]
    logging.error("No such player in battle\n")


def battle_cancel_choosing(bot, update, user_data):
    battle = get_battle(user_data.get('Battle id'))
    player_choosing = get_player_choosing_from_battle_via_id(battle, update.message.from_user.id)
    player_choosing.skill = None
    player_choosing.target = None
    bot.send_message(chat_id=update.message.from_user.id, text="Вы отменили выбор",
                     reply_markup=get_general_battle_buttons(player_choosing.participant))
    user_data.update({'status': 'Battle'})


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
    target = new_target_choosing.participant
    player_choosing.target = target
    user_data.update({'status': 'Battle waiting'})
    bot.send_message(chat_id= update.message.chat_id, text="Вы выбрали цель, ждем других игроков",
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
    dispatcher.bot.send_message(chat_id=player_choosing.participant.id, text="Ждем других игроков",
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
    if team1_alive == 0 and team2_alive > 0:
        return 1
    if team2_alive == 0 and team1_alive > 0:
        return 0



#skill == 6 => пропуск хода
#target == 0 => на себя


def battle_count():     #Тут считается битва в которой все выбрали действие, отдельный процесс, Не забыть сделать так, чтобы выполнялось в таком порядке, в котором было выбрано
                                #Возможно стоит едитить сообщение и проставлять галки для тех, кто уже готов
    try:
        while True:
            battle = battles_need_treating.get()
            team_strings = ["Team 1:\n", "Team 2:\n"]
            result_strings = ["Team 1:\n", "Team 2:\n"]
            for i in battle.skills_queue:
                if i.participant.nickname in battle.dead_list:
                    dispatcher.bot.send_message(chat_id=get_player_choosing_from_battle_via_nick(battle, i.participant.nickname).participant.id, text="Вы мертвы")
                    continue
                i.participant.use_skill(i.skill, i.target)
                if i.target.hp <= 0:
                    battle.dead_list.append(i.target.nickname)
                    target_choosing = get_player_choosing_from_battle_via_id(battle, i.target.id)
                    target_choosing.dead = 1
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
                    dispatcher.bot.sync_send_message(chat_id=player.id,
                                                text=team_strings[0] + team_strings[1],
                                                parse_mode="HTML", reply_markup=get_general_battle_buttons(player))
            result_strings[0] += '\n'
            for i in range(2):
                for j in range(battle.team_players_count):
                    player_choosing = battle.teams[i][j]
                    player = player_choosing.participant
                    interprocess_dictionary = InterprocessDictionary(player.id, "user_data", {'status': 'Battle'})
                    interprocess_queue.put(interprocess_dictionary)
                    dispatcher.bot.sync_send_message(chat_id=player.id, text =result_strings[0] + result_strings[1] +
                                                                         "\n/info_Имя Игрока - информация об игроке",
                                                parse_mode="HTML", reply_markup=get_general_battle_buttons(player))         #TODO Добавить баффы/дебаффы
            res = check_win(battle)
            if res != -1:
                for i in range(2):
                    for j in range(battle.team_players_count):
                        player_choosing = battle.teams[i][j]
                        player = player_choosing.participant
                        dispatcher.bot.sync_send_message(chat_id=player.id, text="{0} команда победила!".format(
                            "Первая" if res == 0 else "Вторая"))
                        interprocess_dictionary = InterprocessDictionary(player.id, "battle status return", {})
                        interprocess_queue.put(interprocess_dictionary)
            else:
                for i in range(2):
                    for j in range(battle.team_players_count):
                        player_choosing = battle.teams[i][j]
                        player = player_choosing.participant
                        interprocess_dictionary = InterprocessDictionary(player.id, "user_data", {'status': 'Battle waiting update'})
                        interprocess_queue.put(interprocess_dictionary)
                treated_battles.put(battle)
    except KeyboardInterrupt:
        return 0


def send_waiting_msg(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Мммм, что это? Race condiotion? (Напишите разрабам, пожалуйста)")


def put_in_pending_battles_from_queue():
    battle = treated_battles.get()
    while battle is not None:
        pending_battles.update({battle.id: battle})
        for i in range(2):
            for j in range(battle.team_players_count):
                player_choosing = battle.teams[i][j]
                player = player_choosing.participant
                interprocess_dictionary = InterprocessDictionary(player.id, "user_data", {'status': 'Battle'})
                interprocess_queue.put(interprocess_dictionary)
        battle = treated_battles.get()
