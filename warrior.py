from libs.player import *

class Warrior(Player):

    def __init__(self, id, username, nickname, sex, race, game_class):
        super(Warrior, self).__init__(id, username, nickname, sex, race, game_class)
        self.target = Player
        self.first_skill_avaliable = 1
        self.second_skill_avaliable = -1
        self.third_skill_avaliable = -1
        self.fourth_skill_avaliable = -1
        self.fifth_skill_avaliable = -1

    def use_first_skill(self):
        self.target.hp -= self.stats["power"] * 3 - self.target.stats["armor"]

    def use_second_skill(self):
        a = 0

    def use_third_skill(self):
        a = 0

    def use_fourth_skill(self):
        a = 0

    def use_fifth_skill(self):
        a = 0

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

