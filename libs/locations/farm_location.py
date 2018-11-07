from libs.locations.location import *

class Farm_Location(Location):
	
	def __init__(self, id, name, lvl):
		super(Farm_Location, self).__init__(id, name)
		self.lvl = lvl
		
		
human_farm_loc_010 = Farm_Location(26, "Локация 0-10", 0)
human_farm_loc_010.roads = [14, 27, 28]
human_farm_loc_1020 = Farm_Location(27, "Локация 10-20", 10)
human_farm_loc_1020.roads = [14, 26, 28, 20]
human_farm_loc_2030 = Farm_Location(28, "Локация 20-30", 20)
human_farm_loc_2030.roads = [17, 30, 21, 26, 27, 29]
human_farm_loc_3040 = Farm_Location(29, "Локация 30-40", 30)
human_farm_loc_3040.roads = [17, 28, 20]
human_farm_loc_4050 = Farm_Location(30, "Локация 40-50", 40)
human_farm_loc_4050.roads = [21, 28, 17]

elf_farm_loc_010 = Farm_Location(31, "Локация 0-10", 0)
elf_farm_loc_010.roads = [15, 32, 33]
elf_farm_loc_1020 = Farm_Location(32, "Локация 10-20", 10)
elf_farm_loc_1020.roads = [15, 31, 33, 22]
elf_farm_loc_2030 = Farm_Location(33, "Локация 20-30", 20)
elf_farm_loc_2030.roads = [18, 35, 23, 31, 32, 34]
elf_farm_loc_3040 = Farm_Location(34, "Локация 30-40", 30)
elf_farm_loc_3040.roads = [18, 33, 22]
elf_farm_loc_4050 = Farm_Location(35, "Локация 40-50", 40)
elf_farm_loc_4050.roads = [23, 33, 18]

orc_farm_loc_010 = Farm_Location(36, "Локация 0-10", 0)
elf_farm_loc_010.roads = [16, 37, 38]
orc_farm_loc_1020 = Farm_Location(37, "Локация 10-20", 10)
elf_farm_loc_1020.roads = [16, 36, 38, 24]
orc_farm_loc_2030 = Farm_Location(38, "Локация 20-30", 20)
elf_farm_loc_2030.roads = [19, 40, 25, 36, 37, 39]
orc_farm_loc_3040 = Farm_Location(39, "Локация 30-40", 30)
elf_farm_loc_3040.roads = [19, 38, 24]
orc_farm_loc_4050 = Farm_Location(40, "Локация 40-50", 40)
elf_farm_loc_4050.roads = [25, 38, 19]
