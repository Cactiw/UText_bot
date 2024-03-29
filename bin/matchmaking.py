from work_materials.globals import dispatcher, matchmaking_players
from libs.interprocess_dictionaty import InterprocessDictionary, interprocess_queue
from libs.battle import BattleStarting
import datetime
import signal
from queue import Empty

MAX_TIME_WITHOUT_PLAYER = datetime.timedelta(minutes=2)

players_in_search_count = {}

def matchmaking():
    try:
        data = matchmaking_players.get()
        waiting_players = [ [], [], [] ]
        battles = []
        while True:
            if data is not None:
                group = data.group
                signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGINT])
                if data.add_to_matchmaking == 0:    # Отмена мачмейкинга

                    for waiting_queue in waiting_players:
                        for player in waiting_queue:
                            if player == data:
                                waiting_queue.remove(player)
                                break
                    for battle in battles:
                        for player_in_battle in battle.players:
                            if player_in_battle.player == data.player:
                                if battle.remove_player(player_in_battle, group) == 1:
                                    battles.remove(battle)
                    dispatcher.user_data.get(data.player.id).update({'status': dispatcher.user_data.get(data.player.id).get('saved_battle_status')})
                    user_data = dispatcher.user_data.get(data.player.id)
                    list_user_data = list(user_data)
                    if 'matchmaking' in list_user_data:
                        user_data.pop('matchmaking')
                    if 'Team' in list_user_data:
                        user_data.pop('Team')
                    try:
                        data = matchmaking_players.get(timeout=datetime.timedelta(minutes=2).total_seconds())
                    except Empty:
                        data = None

                    continue
                                                         #   Добавляю в поиск
                for i in range(0, len(data.game_modes)):
                    if data.game_modes[i]:
                        waiting_players[i].append(data.player)
                battle_mode = 0
                for waiting_queue in waiting_players:
                    for player in waiting_queue:
                        battle_found = 0
                        for battle in battles:
                            if battle.is_suitable(player, battle_mode, group):
                                search_counts = players_in_search_count.get(player.id)
                                if search_counts is None:
                                    search_counts = 0
                                players_in_search_count.update({ player.id : search_counts + 1})
                                battle.add_player(player, group)
                                waiting_queue.remove(player)
                                battle_found = 1
                                if battle.ready_to_start():
                                    battles.remove(battle)
                                    battle.start_battle()


                                    # Удаляю из матчмейкинга в других режимах
                                    for waiting_queue in waiting_players:
                                        for player in waiting_queue:
                                            if player == data.player:
                                                waiting_queue.remove(player)
                                                break


                                    for battle in battles:
                                        for player_in_battle in battle.players:
                                            if player_in_battle.player == data.player:
                                                if battle.remove_player(player_in_battle, group) == 1:
                                                    battles.remove(battle)

                                break
                        if not battle_found:
                            battle = BattleStarting(0, battle_mode)
                            battle.add_player(player, group)
                            waiting_queue.remove(player)
                            battles.append(battle)
                            search_counts = players_in_search_count.get(player.id)
                            if search_counts is None:
                                search_counts = 0
                            players_in_search_count.update({player.id: search_counts + 1})
                    battle_mode += 1
            for battle in battles:
                if datetime.datetime.now() - battle.last_time_player_add >= MAX_TIME_WITHOUT_PLAYER:
                    for player in battle.players:
                        search_counts = players_in_search_count.get(player.player.id)
                        if search_counts == 1:
                            new_status = InterprocessDictionary(player.player.id, "user_data", {"status" : "In Location"})  #TODO сделать вход битву не только из локации
                            interprocess_queue.put(new_status)
                            dispatcher.bot.send_message(chat_id=player.player.id, text = "Игроки для битвы не найдены. Попробуйте позже")
                        else:
                            search_counts -= 1
                            players_in_search_count.update({player.player.id: search_counts})
                    battles.remove(battle)
            signal.pthread_sigmask(signal.SIG_UNBLOCK, [signal.SIGINT])
            try:
                data = matchmaking_players.get(timeout=datetime.timedelta(minutes=2).total_seconds())
            except Empty:
                data = None
    except KeyboardInterrupt:
        return 0
