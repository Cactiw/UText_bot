from libs.locations.location import *
import math

class Capital(Location):
	
    def __init__(self, id, name):
        super(Capital, self).__init__(id, name)
        self.buildings = {"castle" : 1, "barracs" : 1, "tavern" : 1}
        self.progress = {"castle" : [0, 0, 0], "barracs" : [0, 0, 0], "tavern" : [0, 0, 0]}

    def lvl_check(building):
        pass


human_capital = Capital(14, "Столица Людей")
human_capital.roads = [26, 27]
elf_capital = Capital(15, "Столица эльфов")
elf_capital.roads = [31, 32]
orc_capital = Capital(16, "Столица орков")
orc_capital.roads = [36, 37]

