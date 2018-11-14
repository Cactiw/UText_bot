from libs.locations.location import *

class Farm_Location(Location):
	
	def __init__(self, id, name, lvl):
		super(Farm_Location, self).__init__(id, name)
		self.lvl = lvl
		
		
human_farm_loc_010 = Farm_Location(26, "Локация 0-10", 0)
human_farm_loc_010.roads = {14: 5, 27: 6, 28: 12}
human_farm_loc_1020 = Farm_Location(27, "Локация 10-20", 10)
human_farm_loc_1020.roads = {14: 5, 26: 6, 28: 10, 20: 10}
human_farm_loc_2030 = Farm_Location(28, "Локация 20-30", 20)
human_farm_loc_2030.roads = {17: 10, 30: 8, 21: 15, 26: 12, 27: 10, 29: 7}
human_farm_loc_3040 = Farm_Location(29, "Локация 30-40", 30)
human_farm_loc_3040.roads = {17: 5, 28: 7, 20: 10}
human_farm_loc_4050 = Farm_Location(30, "Локация 40-50", 40)
human_farm_loc_4050.roads = {21: 15, 28: 8, 17: 5}

elf_farm_loc_010 = Farm_Location(31, "Локация 0-10", 0)
elf_farm_loc_010.roads = {15: 5, 32: 6, 33: 12}
elf_farm_loc_1020 = Farm_Location(32, "Локация 10-20", 10)
elf_farm_loc_1020.roads = {15: 5, 31: 6, 33: 10, 22: 10}
elf_farm_loc_2030 = Farm_Location(33, "Локация 20-30", 20)
elf_farm_loc_2030.roads = {18: 10, 35: 8, 23: 15, 31: 12, 32: 10, 34: 7}
elf_farm_loc_3040 = Farm_Location(34, "Локация 30-40", 30)
elf_farm_loc_3040.roads = {18: 5, 33: 7, 22: 10}
elf_farm_loc_4050 = Farm_Location(35, "Локация 40-50", 40)
elf_farm_loc_4050.roads = {23: 15, 33: 8, 18: 5}

orc_farm_loc_010 = Farm_Location(36, "Локация 0-10", 0)
elf_farm_loc_010.roads = {16: 5, 37: 6, 38: 12}
orc_farm_loc_1020 = Farm_Location(37, "Локация 10-20", 10)
elf_farm_loc_1020.roads = {16: 5, 36: 6, 38: 10, 24: 10}
orc_farm_loc_2030 = Farm_Location(38, "Локация 20-30", 20)
elf_farm_loc_2030.roads = {19: 10, 40: 8, 25: 15, 36: 12, 37: 10, 39: 7}
orc_farm_loc_3040 = Farm_Location(39, "Локация 30-40", 30)
elf_farm_loc_3040.roads = {19: 5, 38: 7, 24: 10}
orc_farm_loc_4050 = Farm_Location(40, "Локация 40-50", 40)
elf_farm_loc_4050.roads = {25: 15, 38: 8, 19: 5}
