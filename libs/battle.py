import datetime

from work_materials.globals import dispatcher, pending_battles
from work_materials.constants import game_classes_to_emoji
from libs.interprocess_dictionaty import *
import time
import random
from work_materials.buttons.battle_buttons import get_general_battle_buttons
from bin.service_commands import get_player

class Player_in_battle:

    def __init__(self, player, team, group):
        self.player = player
        self.team = team
        self.group = group

    def __eq__(self, other):
        return self.player == other.player


class PlayerChoosing:	#Игрок выбирает ход

    def __init__(self, player, targets, skill, team, number, is_ai=False):
        self.participant = player  #class Player
        self.targets = targets
        self.skill = skill
        self.team = team
        self.number = number
        self.is_ai = is_ai
        self.aggro = 0
        if not self.is_ai:
            self.aggro = player.aggro_prob
            print("player.aggro_prob =", player.aggro_prob)


class Battle:

    def __init__(self, battle_starting):
        self.teams = [ [], [] ]
        self.buff_list = {}         #{nickname: [Buff1, Buff2, ...]}
        self.team_players_count = [len(battle_starting.teams[0]), len(battle_starting.teams[1])]
        for i in range(0, len(battle_starting.teams[0])):
            self.teams[0].append(PlayerChoosing(battle_starting.teams[0][i], None, None, 0, i))
            self.buff_list.update({battle_starting.teams[0][i].nickname: {'power': [],
                                                                          'endurance': [],
                                                                          'armor': [],
                                                                          'charge': [],
                                                                          'speed': []}})
        for i in range(0, len(battle_starting.teams[1])):
            is_ai = battle_starting.mode == "pve"
            self.teams[1].append(PlayerChoosing(battle_starting.teams[1][i], None, None, 1, i + self.team_players_count[0], is_ai))
            self.buff_list.update({battle_starting.teams[1][i].nickname: {'power': [],
                                                                          'endurance': [],
                                                                          'armor': [],
                                                                          'charge': [],
                                                                          'speed': []}})
        self.id = None
        self.aggro_list = {}
        self.mode = battle_starting.mode
        self.last_tick_time = time.time()
        self.skills_queue = []
        self.dead_list = []     #[nickname1, ...]
        self.last_count_time = time.time()
        self.taunt_list = {0: {}, 1: {}}    #{0: {nickname: turns}, 1: {-''-}}
        self.stun_list = {}
        self.damage_change = {}  #{target_nickname: {damage_dealer_nickname: damage, ...}, ...}


    def is_ready(self):
        for team in self.teams:
            for player_choosing in team:
                if not player_choosing.is_ai:
                    if player_choosing.skill is None or player_choosing.targets is None:
                        return False
        self.skills_queue.sort(key=lambda player_choosing: player_choosing.skill.priority)
        return True


class BattleStarting:

    def __init__(self, average_lvl, mode):
        self.players = []
        self.teams = [[], []]
        self.groups = []
        self.teams_avg_lvls = [0, 0]
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

    def add_player(self, player_in, group):
        if group is not None:
            if group.num_players() <= self.need_players - len(self.teams[0]):
                team = 0
            else:
                team = 1
            for player in group.players:
                self.teams[team].append(player)
                player = get_player(player)
                player_in_battle = Player_in_battle(player, team, group)
                self.players.append(player_in_battle)
                self.count += 1
            self.groups.append(group)
            return

        player = Player_in_battle(player_in, -1, group)
        self.players.append(player)
        average_lvl = 0
        self.count = 0

        if player.player.lvl >= self.teams_avg_lvls[0]:
            if self.teams_avg_lvls[0] < self.teams_avg_lvls[1]:
                if len(self.teams[0]) < self.need_players / 2:
                    self.teams[0].append(player.player)
                else:
                    self.teams[1].append(player.player)
            else:
                if len(self.teams[1]) < self.need_players / 2:
                    self.teams[1].append(player.player)
                else:
                    self.teams[0].append(player.player)
        for i in self.players:
            average_lvl += i.player.lvl
            self.count += 1
        self.average_lvl = average_lvl / self.count
        self.last_time_player_add = datetime.datetime.now()

    def remove_player(self, player_in, group):
        if group is not None:
            for player in group.players:
                for pib in self.players:
                    id = pib.player.id
                    if player == id:
                        self.players.remove(pib)
                        self.count -= 1

                        if id in self.teams[0]:
                            self.teams[0].remove(id)
                        elif id in self.teams[1]:
                            self.teams[1].remove(id)
                        continue
        else:
            self.players.remove(player_in)
        average_lvl = 0
        self.count = 0
        for i in self.players:
            average_lvl += i.player.lvl
            self.count += 1
        if self.count == 0:
            return 1
        self.average_lvl = average_lvl / self.count

    def is_suitable(self, player, battle_mode, group):
        free_places_in_teams = [self.need_players - len(self.teams[0]), self.need_players - len(self.teams[1])]
        if group is None:
            return abs(player.lvl - self.average_lvl) <= 2 and self.mode == battle_mode and \
            (self.teams_avg_lvls[0] <= self.teams_avg_lvls[1] and player.lvl > self.teams_avg_lvls[0] and free_places_in_teams[0] >= 1) or \
            (self.teams_avg_lvls[0] > self.teams_avg_lvls[1] and player.lvl > self.teams_avg_lvls[1] and free_places_in_teams[1] >= 1)     #   Пока норм, можно дальше чекать

        else:
            return self.mode == battle_mode and abs(group.avg_lvl() - self.average_lvl) <= 2 and len(group.players) <= self.need_players - self.count and \
                (free_places_in_teams[0] >= len(group.players) or free_places_in_teams[1] >= len(group.players)) and \
                ((self.teams_avg_lvls[0] < self.teams_avg_lvls[1] and group.avg_lvl() > self.teams_avg_lvls[0] and free_places_in_teams[0] >= group.num_players()) or
                (self.teams_avg_lvls[0] > self.teams_avg_lvls[1] and group.avg_lvl() > self.teams_avg_lvls[1] and free_places_in_teams[1] >= group.num_players()))

    def ready_to_start(self):
        return self.count >= self.need_players

    def start_battle(self):
        self.teams_avg_lvls = [0, 0]
        self.teams_sum_lvls = [0, 0]
        self.players_need_to_be_distributed = self.players.copy()
        self.teams[0].clear()
        self.teams[1].clear()
        self.players.sort(key=lambda player_in_battle: player_in_battle.player.lvl)
        for group in self.groups:
            if (self.need_players / 2) - len(self.teams[0]) >= group.num_players():
                team = 0
            else:
                team = 1
            for player_id in group.players:
                player = get_player(player_id)
                player_in_battle = Player_in_battle(player, team, group)
                self.teams[team].append(player)
                self.teams_sum_lvls[team] += player.lvl
                self.teams_avg_lvls[team] = 0
                count = 0
                for j in self.teams[team]:
                    self.teams_avg_lvls[team] += j.lvl
                    count += 1
                self.teams_avg_lvls[team] /= count
                self.players_need_to_be_distributed.remove(player_in_battle)
        self.players_need_to_be_distributed.sort(key=lambda player_in_battle: player_in_battle.player.lvl, reverse=True)
        for i in range(len(self.players_need_to_be_distributed)):
            if self.teams_sum_lvls[0] <= self.teams_sum_lvls[1] and len(self.teams[0]) < (self.need_players / 2):
                self.teams[0].append(self.players_need_to_be_distributed[i].player)
                self.teams_sum_lvls[0] += self.players_need_to_be_distributed[i].player.lvl
                self.teams_avg_lvls[0] = 0
                count = 0
                for j in self.teams[0]:
                    self.teams_avg_lvls[0] += j.lvl
                    count += 1
                self.teams_avg_lvls[0] /= count
            else:
                self.teams[1].append(self.players_need_to_be_distributed[i].player)
                self.teams_sum_lvls[1] += self.players_need_to_be_distributed[i].player.lvl
                self.teams_avg_lvls[1] = 0
                count = 0
                for j in self.teams[1]:
                    self.teams_avg_lvls[1] += j.lvl
                    count += 1
                self.teams_avg_lvls[1] /= count

        team1_text = "Противники найдены, битва начинается!\nВаша команда:\n"
        team2_text = "Противники найдены, битва начинается!\nВаша команда:\n"
        battle = Battle(self)
        j = 0
        for i in self.teams[0]:
            team1_text += "<b>{0}</b>{4} {1}🔺️  {2}🌡 {3}⚡  /info_{5}\n".format(i.nickname, i.lvl, i.hp, i.charge,
                                                                      game_classes_to_emoji.get(i.game_class), battle.teams[0][j].number)
            j += 1
        team1_text += "\nВаши соперники:\n"
        j = 0
        for i in self.teams[1]:
            team1_text += "<b>{0}</b>{4}  {1}🔺️   {2}🌡 {3}⚡  /info_{5}\n".format(i.nickname, i.lvl, i.hp, i.charge,
                                                                       game_classes_to_emoji.get(i.game_class), battle.teams[1][j].number)
            team2_text += "<b>{0}</b>{4}  {1}🔺   {2}🌡 {3}⚡  /info_{5}\n".format(i.nickname, i.lvl, i.hp, i.charge,
                                                                      game_classes_to_emoji.get(i.game_class), battle.teams[1][j].number)
            j += 1
        team2_text += "\nВаши соперники:\n"
        j = 0
        for i in self.teams[0]:
            team2_text += "<b>{0}</b>{4}  {1}🔺  {2}🌡 {3}⚡  /info_{5}\n".format(i.nickname, i.lvl, i.hp, i.charge,
                                                                     game_classes_to_emoji.get(i.game_class), battle.teams[0][j].number)
            j += 1
        j = 0
        """team1_text += "\n/info_Имя Игрока - информация об игроке"`
        team2_text += "\n/info_Имя Игрока - информация об игроке"""
        self.start_battle_without_balance(battle, team1_text, team2_text)


    def start_battle_without_balance(self, battle, team1_text = "Начинается битва!", team2_text = ""):
        num_teams_to_send_messages = 2
        if self.mode == "pve":
            num_teams_to_send_messages = 1
        for j in range(num_teams_to_send_messages):
            for i in self.teams[j]:
                dispatcher.bot.sync_send_message(chat_id=i.id, text=team1_text if not j else team2_text, parse_mode='HTML', reply_markup = get_general_battle_buttons(i))
                interprocess_dictionary = InterprocessDictionary(i.id, "user_data", {"status" : "Battle"})
                interprocess_queue.put(interprocess_dictionary)
                status = InterprocessDictionary(i.id, "user_data", {'Team': j})
                interprocess_queue.put(status)
        battle_id = random.randint(1, 4294967295)
        ids = list(pending_battles)
        while battle_id in ids:
            battle_id = random.randint(1, 4294967295)
        self.id = battle_id
        battle.id = self.id
        for player in self.players:
            try:
                player = player.player
            except AttributeError:
                pass
            player.battle_id = battle_id
            player.update_cooldown()
            interprocess_dictionary = InterprocessDictionary(player.id, "user_data", {'Battle id': battle_id})
            interprocess_queue.put(interprocess_dictionary)
        battle_status = InterprocessDictionary(None, "battles_pending", {battle_id: battle})
        interprocess_queue.put(battle_status)
