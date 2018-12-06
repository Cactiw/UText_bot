from libs.player import *
from work_materials.globals import *


class Player_in_battle:

    def __init__(self, player, team):
        self.player = player
        self.team = team

    def __eq__(self, other):
        return self.player == other.player


class Battle:
    players = []
    count = 0
    def __init__(self, average_lvl, need_players):
        self.average_lvl = average_lvl
        self.need_players = need_players
        self.teams = [int(need_players / 2), int(need_players / 2)]


    def add_player(self, player_in):
        player = Player_in_battle(player_in, -1)
        self.players.append(player)
        average_lvl = 0
        self.count = 0
        for i in range(0, len(self.teams)):
            if self.teams[i] > 0:
                player.team = i
                self.teams[i] -= 1
                break
        for i in self.players:
            average_lvl += i.player.lvl
            self.count += 1
        self.average_lvl = average_lvl / self.count


    def remove_player(self, player_in):
        self.teams[player_in.team] += 1
        self.players.remove(player_in)
        average_lvl = 0
        self.count = 0
        for i in self.players:
            average_lvl += i.player.lvl
            self.count += 1
        if self.count == 0:
            return 1
        self.average_lvl = average_lvl / self.count

    def ready_to_start(self):
        return self.count >= self.need_players

    def start_battle(self):
        for i in self.players:
            dispatcher.bot.send_message(chat_id=i.player.id, text="Противники найдены, битва начинается!\nВаша команда :{0}".format(i.team))