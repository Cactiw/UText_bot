from libs.locations.location import *

class Tower(Location):

	def __init__(self, id, name, fraction):
		super(Tower, self).__init__(id, name)
		self.fraction = fraction  #фракция, которая контроллирует точку


feds_south_tower = Tower(5, "Южная башня людей", "Федералы")
feds_south_tower.roads = {6: 3, 2: 5, 11: 7, 17: 10}
feds_north_tower = Tower(6, "Северная башня людей", "Федералы")
feds_north_tower.roads = {5: 3, 2: 5, 13: 7, 17: 10}
trib_south_tower = Tower(7, "Южная башня эльфов", "elves")
trib_south_tower.roads = {11: 7, 3: 5, 8: 3, 18: 10}
trib_north_tower = Tower(8, "Северная башня эльфов", "elves")
trib_north_tower.roads = {12: 7, 3: 5, 7: 3, 18: 10}
stai_south_tower = Tower(9, "Южная башня орков", "stais")
stai_south_tower.roads = {13: 7, 4: 5, 10: 3, 19: 10}
stai_north_tower = Tower(10, "Северная башня орков", "stais")
stai_north_tower.roads = {12: 7, 4: 5, 9: 3, 19: 10}
