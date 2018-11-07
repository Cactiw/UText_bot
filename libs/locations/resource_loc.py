from libs.locations.location import *


class Resource_Loc(Location):

    def __init__(self, id, name, fraction):
        super(Resource_Loc, self).__init__(id, name)
        self.type = None
        self.fraction = fraction #фракция, которая контроллирует точку

    def change_fraction(self, new_fraction):
        self.fraction = new_fraction


resources_btw_HE = Resource_Loc(11, "Ресурсы между людьми и эльфами", None)
resources_btw_HE.roads = [5, 2, 3, 7]
resources_btw_EO = Resource_Loc(12, "Ресурсы между эльфами и орками", None)
resources_btw_EO.roads = [8, 3, 4, 10]
resources_btw_HO = Resource_Loc(13, "Ресурсы между людьми и орками", None)
resources_btw_HO.roads = [9, 4, 2, 6]

human_forest = Resource_Loc(20, "Лес", "humans")
human_forest.roads = [27, 29]
human_mine = Resource_Loc(21, "Шахта", "humans")
human_mine.roads = [28, 30]
elf_forest = Resource_Loc(22, "Лес", "elves")
elf_forest.roads = [32, 34]
elf_mine = Resource_Loc(23, "Шахта", "elves")
elf_mine.roads = [33, 35]
orc_forest = Resource_Loc(24, "Лес", "orcs")
orc_forest.roads = [37, 39]
orc_mine = Resource_Loc(25, "Шахта", "orcs")
orc_mine.roads = [38, 40]