from work_materials.globals import interprocess_queue, dispatcher
from libs.interprocess_dictionaty import InterprocessDictionary
from libs.battle import matchmaking_players, BattleStarting
import datetime
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
                if data.add_to_matchmaking == 0:

                    for waiting_queue in waiting_players:
                        for player in waiting_queue:
                            if player == data:
                                waiting_queue.remove(player)
                                break
                    for battle in battles:
                        for player_in_battle in battle.players:
                            if player_in_battle.player == data.player:
                                if battle.remove_player(player_in_battle) == 1:
                                    battles.remove(battle)
                    try:
                        data = matchmaking_players.get(timeout=datetime.timedelta(minutes=2).total_seconds())
                    except Empty:
                        data = None
                    continue
                                                         #   Добавляю в поиск
                for i in range(0, len(data.game_modes)):
                    if data.game_modes[i]:
                        waiting_players[i].append(data.player)
                        print("put into queue", i)
                group = data.group
                battle_mode = 0
                for waiting_queue in waiting_players:
                    for player in waiting_queue:
                        print("in player")
                        battle_found = 0
                        for battle in battles:
                            print(abs(player.lvl - battle.average_lvl))
                            if battle.is_suitable(player, battle_mode, group):
                                print("adding player", player.nickname,  ",mode =", battle_mode)
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
                                                if battle.remove_player(player_in_battle) == 1:
                                                    battles.remove(battle)

                                break
                        if not battle_found:
                            print("not found")
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
            try:
                data = matchmaking_players.get(timeout=datetime.timedelta(minutes=2).total_seconds())
            except Empty:
                data = None
    except KeyboardInterrupt:
        return 0
