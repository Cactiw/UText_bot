from libs.locations.location import *
import math

class Guild_Castle(Location):

    def __init__(self, id, name):
        super(Guild_Castle, self).__init__(id, name)
        self.buildings = {"forge": 1, "alchemy_station": 1, "enchantment_station": 1}
        self.progress = {"forge": [0, 0, 0], "alchemy_station": [0, 0, 0], "enchantment_station": [0, 0, 0]}  #[gold, wood, metal]

    @staticmethod
    def lvl_up(self, building):
        lvl = self.buildings.get(building)
        self.buildings[building] += 1
        self.progress[building][0] -= int((math.log(lvl, math.e) ** 5) * (lvl ** 3) + 4421 * lvl)
        self.progress[building][1] -= int((math.log(lvl, math.e) ** 5) * (lvl ** 3) + 5432 * lvl)
        self.progress[building][2] -= int((math.log(lvl, math.e) ** 5) * (lvl ** 3) + 3498 * lvl)

    def lvl_check(self, building):
        lvl = self.buildings.get(building)
        if lvl < 15:
            flag = 1
            if self.progress.get(building)[0] < int((math.log(lvl + 1, math.e) ** 5)
                                            * ((lvl + 1) ** 3) + 4421 * (lvl + 1)):
                flag = 0
            if self.progress.get(building)[1] < int((math.log(lvl + 1, math.e) ** 5)
                                            * ((lvl + 1) ** 3) + 5432 * (lvl + 1)):
                flag = 0
            if self.progress.get(building)[2] < int((math.log(lvl + 1, math.e) ** 5)
                                            * ((lvl + 1) ** 3) + 3498 * (lvl + 1)):
                flag = 0
            if flag == 1:
                self.lvl_up(self, building)
            else:
                return 0
        else:
            return 0


human_guild_castle = Guild_Castle(17, "Замок гильдии")
human_guild_castle.roads = [5, 6, 28, 29, 30]
elf_guild_castle = Guild_Castle(18, "Замок Гильдии")
elf_guild_castle.roads = [7, 8, 33, 34, 35]
orc_guild_castle = Guild_Castle(19, "Замок Гильдии")
orc_guild_castle.roads = [9, 10, 38, 39, 40]