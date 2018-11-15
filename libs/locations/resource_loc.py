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

feds_forest = Resource_Loc(20, "Лес", "Федералы")
feds_forest.roads = {27: 10, 29: 10}
feds_mine = Resource_Loc(21, "Шахта", "Федералы")
feds_mine.roads = {28: 15, 30: 15}
trib_forest = Resource_Loc(22, "Лес", "Трибунал")
trib_forest.roads = {32: 10, 34: 10}
trib_mine = Resource_Loc(23, "Шахта", "Трибунал")
trib_mine.roads = {33: 15, 35: 15}
stai_forest = Resource_Loc(24, "Лес", "Стая")
stai_forest.roads = {37: 10, 39: 10}
stai_mine = Resource_Loc(25, "Шахта", "Стая")
stai_mine.roads = {38: 15, 40: 15}