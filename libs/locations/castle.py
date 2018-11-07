from libs.locations.location import *


class Castle(Location):

    def __init__(self, id, name, fraction):
        super(Castle, self).__init__(id, name)
        self.fraction = fraction  #фракция, которая контроллирует точку

    def change_fraction(self, new_fraction):
        self.fraction = new_fraction


human_castle = Castle(2, "Замок людей", "humans")
human_castle.roads = [1, 11, 13, 5, 6]
elf_castle = Castle(3, "Замок эльфов", "elves")
elf_castle.roads = [1, 11, 12, 7, 8]
orc_castle = Castle(4, "Замок орков", "orcs")
orc_castle.roads = [1, 12, 13, 9, 10]