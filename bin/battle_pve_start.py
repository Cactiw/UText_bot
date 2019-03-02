from libs.battle import Battle, BattleStarting

def battle_pve_start(players, enemies):
    battle = BattleStarting(0, "pve")
    for player in players:
        battle.teams[0].append(player)
        battle.players.append(player)
    for i in range(len(enemies)):
        enemy = enemies[i]
        enemy.nickname += " {0}".format(i)
        battle.teams[1].append(enemy)
    final_battle = Battle(battle)
    battle.start_battle_without_balance(final_battle)
