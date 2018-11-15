from libs.locations.location import *


class Castle(Location):

    def __init__(self, id, name, fraction):
        super(Castle, self).__init__(id, name)
        self.fraction = fraction  #фракция, которая контроллирует точку

    def change_fraction(self, new_fraction):
        self.fraction = new_fraction


feds_castle = Castle(2, "Замок людей", "Федералы")
feds_castle.roads = {1: 8, 11: 5, 13: 5, 5: 5, 6: 5}
trib_castle = Castle(3, "Замок эльфов", "Трибунал")
trib_castle.roads = {1: 8, 11: 5, 12: 5, 7: 5, 8: 5}
stai_castle = Castle(4, "Замок орков", "Стая")
stai_castle.roads = {1: 8, 12: 5, 13: 5, 9: 5, 10: 5}