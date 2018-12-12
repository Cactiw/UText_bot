from libs.battle import BattleStarting, Player_in_battle
from libs.player import Player
from work_materials.globals import battles_need_treating
import time


battle = None

class PlayerChoosing:
	def __init__(self, player_in_battle, target, skill):
		self.participant = player_in_battle
		self.target = target
		self.skill = skill

class Battle:
	def __init__(self, battle_starting):
		self.team1 = []
		self.team2 = []
		for i in range(len(battle_starting.team1)):
			self.team1[i] = PlayerChoosing(battle_starting.team1[i], None, None)
			self.team1[i] = PlayerChoosing(battle_starting.team1[i], None, None)
		self.players_number = len(self.team1)
		self.last_update_time = time.time()



def start_battle(battle_starting):
	global battle
	battle = Battle(battle_starting)
	for i in range(battle.players_number):
		pass



