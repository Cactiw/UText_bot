from libs.locations.location import *

class Tower(Location):

	def __init__(self, id, name, fraction):
		super(Tower, self).__init__(id, name)
		self.fraction = fraction  #фракция, которая контроллирует точку


human_south_tower = Tower(5, "Южная башня людей", "humans")
human_south_tower.roads = [6, 2, 11, 17]
human_north_tower = Tower(6, "Северная башня людей", "humans")
human_north_tower.roads = [5, 2, 13, 17]
elf_south_tower = Tower(7, "Южная башня эльфов", "elves")
elf_south_tower.roads = [11, 3, 8, 18]
elf_north_tower = Tower(8, "Северная башня эльфов", "elves")
elf_north_tower.roads = [12, 3, 7, 18]
orcs_south_tower = Tower(9, "Южная башня орков", "orcs")
orcs_south_tower.roads = [13, 4, 10, 19]
orcs_north_tower = Tower(10, "Северная башня орков", "orcs")
orcs_north_tower.roads = [13, 4, 9, 19]
