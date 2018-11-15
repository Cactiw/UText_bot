from libs.locations.location import *

class Tower(Location):

	def __init__(self, id, name, fraction):
		super(Tower, self).__init__(id, name)
		self.fraction = fraction  #фракция, которая контроллирует точку


human_south_tower = Tower(5, "Южная башня людей", "humans")
human_south_tower.roads = {6: 3, 2: 5, 11: 7, 17: 10}
human_north_tower = Tower(6, "Северная башня людей", "humans")
human_north_tower.roads = {5: 3, 2: 5, 13: 7, 17: 10}
elf_south_tower = Tower(7, "Южная башня эльфов", "elves")
elf_south_tower.roads = {11: 7, 3: 5, 8: 3, 18: 10}
elf_north_tower = Tower(8, "Северная башня эльфов", "elves")
elf_north_tower.roads = {12: 7, 3: 5, 7: 3, 18: 10}
orc_south_tower = Tower(9, "Южная башня орков", "orcs")
orc_south_tower.roads = {13: 7, 4: 5, 10: 3, 19: 10}
orc_north_tower = Tower(10, "Северная башня орков", "orcs")
orc_north_tower.roads = {12: 7, 4: 5, 9: 3, 19: 10}
