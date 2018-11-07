from libs.locations.location import *

class Guild_Castle(Location):
	
	def __init__(self, id, name):
		super(Guild_Castle, self).__init__(id, name)
		self.buildings = {"forge" : 1, "alchemy_station": 1, "enchantment_station" : 1}

human_guild_castle = Guild_Castle(17, "Замок гильдии")
human_guild_castle.roads = [5, 6, 28, 29, 30]
elf_guild_castle = Guild_Castle(18, "Замок Гильдии")
elf_guild_castle.roads = [7, 8, 33, 34, 35]
orc_guild_castle = Guild_Castle(19, "Замок Гильдии")
orc_guild_castle.roads = [9, 10, 38, 39, 40]