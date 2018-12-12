from libs.battle import Battle, Player_in_battle
from libs.player import Player


class PlayerChoosing:
	def __init__(self, player_in_battle, target, skill):
		self.participant = player_in_battle
		self.target = target
		self.skill = skill


def process_battle(battle):
	team1 = []
	team2 = []
	for i in range(len(battle.players)):
		if battle.players[i].team == 1:
			team1.append(battle.players[i].player)
		else:
			team2.append(battle.players[i].player)



