from work_materials.globals import *
from libs.player_matchmaking import *
from libs.battle import *

def matchmaking():
    data = matchmaking_players.get()
    waiting_players = [ [], [], [] ]
    battles = []
    while data is not None:
        print("got player")
        print(data.add_to_matchmaking)
        if data.add_to_matchmaking == 0:
            print("Trying to delete... skiped")

            for waiting_queue in waiting_players:
                for player in waiting_queue:
                    if player == data:
                        print("removing from queue")
                        waiting_queue.remove(player)
                        break
            for battle in battles:
                for player_in_battle in battle.players:
                    if player_in_battle.player == data.player:
                        print("removing from battle")
                        if battle.remove_player(player_in_battle) == 1:
                            battles.remove(battle)

            data = matchmaking_players.get()
            continue
        for i in range(0, len(data.game_modes)):
            if data.game_modes[i]:
                waiting_players[i].append(data.player)
                print("put into queue", i)


        for waiting_queue in waiting_players:
            for player in waiting_queue:

                battle_found = 0
                for battle in battles:
                    print(abs(player.lvl - battle.average_lvl))
                    if abs(player.lvl - battle.average_lvl) <= 2:
                        battle.add_player(player)
                        waiting_queue.remove(player)
                        battle_found = 1
                        if battle.ready_to_start():
                            battles.remove(battle)
                            battle.start_battle()
                        break
                if not battle_found:
                    print("creating battle")
                    battle = Battle(0, 2)
                    battle.add_player(player)
                    waiting_queue.remove(player)
                    battles.append(battle)
                    print(battle.average_lvl)

        data = matchmaking_players.get()