from libs.locations.location import *
import math


class Capital(Location):

    def __init__(self, id, name):
        super(Capital, self).__init__(id, name)
        self.buildings = {"castle": 1, "barracs": 1, "tavern": 1}
        self.progress = {"castle": [0, 0, 0], "barracs": [0, 0, 0], "tavern": [0, 0, 0]} #[gold, wood, metal]

    @staticmethod
    def lvl_up(self, building):
        lvl = self.buildings.get(building)
        self.buildings[building] += 1
        self.progress[building][0] -= int((math.log(lvl, math.e) ** 5)
                                          * (lvl ** 3) + 4421 * (lvl ** 3) / math.log(lvl, math.e))
        self.progress[building][1] -= int((math.log(lvl, math.e) ** 5)
                                          * (lvl ** 3) + 5432 * (lvl ** 3) / math.log(lvl, math.e))
        self.progress[building][2] -= int((math.log(lvl, math.e) ** 5)
                                          * (lvl ** 3) + 3498 * (lvl ** 3) / math.log(lvl, math.e))

    def lvl_check(self, building):
        lvl = self.buildings.get(building)
        if lvl < 15:
            flag = 1
            if self.progress.get(building)[0] < int((math.log(lvl + 1, math.e) ** 5)
                                    * ((lvl + 1) ** 3) + 4421 * ((lvl + 1) ** 3) / math.log(lvl + 1, math.e)):
                flag = 0
            if self.progress.get(building)[1] < int((math.log(lvl + 1, math.e) ** 5)
                                    * ((lvl + 1) ** 3) + 5432 * ((lvl + 1) ** 3) / math.log(lvl + 1, math.e)):
                flag = 0
            if self.progress.get(building)[2] < int((math.log(lvl + 1, math.e) ** 5)
                                    * ((lvl + 1) ** 3) + 3498 * ((lvl + 1) ** 3) / math.log(lvl + 1, math.e)):
                flag = 0
            if flag == 1:
                self.lvl_up(self, building)
            else:
                return 0
        else:
            return 0


feds_capital = Capital(14, "Столица людей")
feds_capital.roads = {26: 5, 27: 5}
trib_capital = Capital(15, "Столица эльфов")
trib_capital.roads = {31: 5, 32: 5}
stai_capital = Capital(16, "Столица орков")
stai_capital.roads = {36: 5, 37: 5}

