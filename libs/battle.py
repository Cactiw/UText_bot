import datetime

from libs.player import *
from work_materials.globals import *
from libs.status_interprocess import *
from bin.show_general_buttons import show_general_buttons
import time
import random
from work_materials.buttons.battle_buttons import get_general_battle_buttons

class Player_in_battle:

    def __init__(self, player, team):
        self.player = player
        self.team = team

    def __eq__(self, other):
        return self.player == other.player


class PlayerChoosing:	#Игрок выбирает ход

    def __init__(self, player_in_battle, target, skill):
        self.participant = player_in_battle
        self.target = target
        self.skill = skill


class Battle:

    def __init__(self, battle_starting):
        self.teams = [ [], [] ]
        for i in range(0, len(battle_starting.team1)):
            self.teams[0].append(PlayerChoosing(battle_starting.team1[i], None, None))
            self.teams[1].append(PlayerChoosing(battle_starting.team2[i], None, None))
        self.team_players_count = len(self.teams[0])
        self.last_tick_time = time.time()

    def is_ready(self):
        for team in self.teams:
            for player_choosing in team:
                if player_choosing.skill is None or player_choosing.target is None:
                    return False
        return True


class BattleStarting:

    def __init__(self, average_lvl, mode):
        self.players = []
        self.team1 = []
        self.team2 = []
        self.average_lvl = average_lvl
        self.mode = mode
        self.count = 0
        self.starting_flag = 1
        self.last_time_player_add = datetime.datetime.now()
        if self.mode == 0:
            self.need_players = 2
        elif self.mode == 1:
            self.need_players = 6
        else:
            self.need_players = 10
        self.__teams = [int(self.need_players / 2), int(self.need_players / 2)]
        print(self.mode, self.need_players, self.__teams)

    def add_player(self, player_in):
        player = Player_in_battle(player_in, -1)
        self.players.append(player)
        average_lvl = 0
        self.count = 0
        for i in range(0, len(self.__teams)):
            if self.__teams[i] > 0:
                player.team = i
                self.__teams[i] -= 1
                break
        for i in self.players:
            average_lvl += i.player.lvl
            self.count += 1
        self.average_lvl = average_lvl / self.count
        self.last_time_player_add = datetime.datetime.now()
        print("battle =,", self)
        print("battle.players =", self.players, ", mode =", self.mode)

    def remove_player(self, player_in):
        self.__teams[player_in.team] += 1
        self.players.remove(player_in)
        average_lvl = 0
        self.count = 0
        for i in self.players:
            average_lvl += i.player.lvl
            self.count += 1
        if self.count == 0:
            return 1
        self.average_lvl = average_lvl / self.count

    def is_suitable(self, player, battle_mode):
        return abs(player.lvl - self.average_lvl) <= 2 and self.mode == battle_mode

    def ready_to_start(self):
        return self.count >= self.need_players

    def start_battle(self):
        self.players.sort(key = lambda player_in_battle: player_in_battle.player.lvl)
        if self.need_players > 2:
            for i in range(0, len(self.players), 2):
                self.players[i].team = 0
                self.players[i + 1].team = 1

        for i in self.players:
            if not i.team:
                self.team1.append(i.player)
            else:
                self.team2.append(i.player)
        team1_text = "Противники найдены, битва начинается!\nВаша команда:\n"
        team2_text = "Противники найдены, битва начинается!\nВаша команда:\n"
        for i in self.team1:
            team1_text += "<b>{0}</b> lvl: {1}\n".format(i.nickname, i.lvl)
        team1_text += "\nВаши соперники:\n"
        for i in self.team2:
            team1_text += "<b>{0}</b> lvl: {1}\n".format(i.nickname, i.lvl)
            team2_text += "<b>{0}</b> lvl: {1}\n".format(i.nickname, i.lvl)
        team2_text += "\nВаши соперники:\n"
        for i in self.team1:
            team2_text += "<b>{0}</b> lvl: {1}\n".format(i.nickname, i.lvl)
        for i in self.team1:
            dispatcher.bot.sync_send_message(chat_id=i.id, text=team1_text, parse_mode='HTML', reply_markup = get_general_battle_buttons(i))
            #show_general_buttons(bot, i.id, {"status" : "Battle"})
            status = StatusInterprocess(i.id, {"status" : "Battle"})
            statuses.put(status)
            dispatcher.user_data.get(i.id).update({'Team': 0})
        for i in self.team2:
            dispatcher.bot.sync_send_message(chat_id=i.id, text=team2_text, parse_mode='HTML', reply_markup = get_general_battle_buttons(i))
            #show_general_buttons(bot, i.id, {"status" : "Battle"})
            status = StatusInterprocess(i.id, {"status" : "Battle"})
            statuses.put(status)
            dispatcher.user_data.get(i.id).update({'Team': 1})
        self.players.clear()
        battle = Battle(self)
        battle_id = random.randint(1, 4294967295)
        ids = list(pending_battles)
        while battle_id in ids:
            battle_id = random.randint(1, 4294967295)
        for player in self.players:
            player.battle_id = battle_id
            dispatcher.user_data.get(player.id).update({'Battle id': battle_id})
        pending_battles.update({battle_id: battle})
