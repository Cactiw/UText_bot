from libs.locations.location import *

class Guild_Castle(Location):
	
	def __init__(self, id, name):
		super(Guild_Castle, self).__init__(id, name)
		self.buildings = {"forge" : 1, "alchemy_station": 1, "enchantment_station" : 1}

human_guild_castle = Guild_Castle(17, "Замок гильдии")
elf_guild_castle = Guild_Castle(18, "Замок Гильдии")
orc_guild_castle = Guild_Castle(19, "Замок Гильдии")