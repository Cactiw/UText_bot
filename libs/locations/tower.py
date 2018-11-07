from libs.locations.location import *

class Tower(Location):

	def __init__(self, id, name, fraction):
		super(Tower, self).__init__(id, name)
		self.fraction = fraction  #фракция, которая контроллирует точку


south_human_tower = Tower(5, "Южная башня людей", "humans")
north_human_tower = Tower(6, "Северная башня людей", "humans")
south_elf_tower = Tower(7, "Южная башня эльфов", "elves")
north_elf_tower = Tower(8, "Северная башня эльфов", "elves")
south_orcs_tower = Tower(9, "Южная башня орков", "orcs")
north_orcs_tower = Tower(10, "Северная башня орков", "orcs")
