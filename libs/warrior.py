from libs.player import *

class Warrior(Player):

    def __init__(self, id, username, nickname, sex, race, game_class):
        super(Warrior, self).__init__(id, username, nickname, sex, race, game_class)
        self.target = Player
        self.first_skill_lvl = 1        #TODO add to database
        self.second_skill_lvl = 1
        self.third_skill_lvl = 0
        self.fourth_skill_lvl = 0
        self.fifth_skill_lvl = 0

    def use_first_skill(self):
        '''damage = self.stats["power"] * 3 - self.target.stats["armor"]
        if self.target.take_damage_by_armor >= damage:
            self.target.take_damage_by_armor -= damage
        else:
            damage -= self.target.take_damage_by_armor
            self.target.take_damage_by_armor = 0
            self.target.hp -= damage'''
        a = 0       #TODO damage

    def use_second_skill(self):
        a = 0       #TODO stan

    def use_third_skill(self):
        a = 0       #TODO shield

    def use_fourth_skill(self):
        a = 0       #TODO argo

    def use_fifth_skill(self):
        a = 0       #TODO AOE

    def use_skill(self, text):
        if text == "first":
            self.use_first_skill()
        elif text == "second":
            self.use_second_skill()
        elif text == "third":
            self.use_third_skill()
        elif text == "fourth":
            self.use_fourth_skill()
        elif text == "fifth":
            self.use_fifth_skill()

