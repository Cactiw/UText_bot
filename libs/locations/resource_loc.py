from libs.locations.location import *

class Resource_Loc(Location):

	def __init__(self, id, name, fraction):
		super(Resource_Loc, self).__init__(id, name)
		self.type = None
		self.fraction = fraction #фракция, которая контроллирует точку


resources_btw_HE = Resource_Loc(11, "Ресурсы между людьми и эльфами", None)
resources_btw_EO = Resource_Loc(12, "Ресурсы между эльфами и орками", None)
resources_btw_HO = Resource_Loc(13, "Ресурсы между людьми и орками", None)

human_forest = Resource_Loc(20, "Лес", "humans")
human_mine = Resource_Loc(21, "Шахта", "humans")
elf_forest = Resource_Loc(22, "Лес", "elves")
elf_mine = Resource_Loc(23, "Шахта", "elves")
orc_forest = Resource_Loc(24, "Лес", "orcs")
orc_mine = Resource_Loc(25, "Шахта", "orcs")