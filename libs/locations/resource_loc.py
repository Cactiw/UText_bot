from libs.locations.location import *


class Resource_Loc(Location):

    def __init__(self, id, name, fraction):
        super(Resource_Loc, self).__init__(id, name)
        self.type = None
        self.fraction = fraction #фракция, которая контроллирует точку

    def change_fraction(self, new_fraction):
        self.fraction = new_fraction


resources_btw_HE = Resource_Loc(11, "Ресурсы между людьми и эльфами", None)
resources_btw_HE.roads = {5: 7, 2: 5, 3: 5, 7: 7}
resources_btw_EO = Resource_Loc(12, "Ресурсы между эльфами и орками", None)
resources_btw_EO.roads = {8: 7, 3: 5, 4: 5, 10: 7}
resources_btw_HO = Resource_Loc(13, "Ресурсы между людьми и орками", None)
resources_btw_HO.roads = {9: 7, 4: 5, 2: 5, 6: 7}

human_forest = Resource_Loc(20, "Лес", "humans")
human_forest.roads = {27: 10, 29: 10}
human_mine = Resource_Loc(21, "Шахта", "humans")
human_mine.roads = {28: 15, 30: 15}
elf_forest = Resource_Loc(22, "Лес", "elves")
elf_forest.roads = {32: 10, 34: 10}
elf_mine = Resource_Loc(23, "Шахта", "elves")
elf_mine.roads = {33: 15, 35: 15}
orc_forest = Resource_Loc(24, "Лес", "orcs")
orc_forest.roads = {37: 10, 39: 10}
orc_mine = Resource_Loc(25, "Шахта", "orcs")
orc_mine.roads = {38: 15, 40: 15}