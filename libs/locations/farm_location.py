from libs.locations.location import *

class Farm_Location(Location):
	
	def __init__(self, id, name, lvl):
		super(Farm_Location, self).__init__(id, name)
		self.lvl = lvl
		
		
feds_farm_loc_010 = Farm_Location(26, "Главное полицейское управление", 0)
feds_farm_loc_010.roads = {14: 5, 27: 6, 28: 12}
feds_farm_loc_1020 = Farm_Location(27, "Квартал Единства", 10)
feds_farm_loc_1020.roads = {14: 5, 26: 6, 28: 10, 20: 10}
feds_farm_loc_2030 = Farm_Location(28, "Центральная площадь", 20)
feds_farm_loc_2030.roads = {17: 10, 30: 8, 21: 15, 26: 12, 27: 10, 29: 7}
feds_farm_loc_3040 = Farm_Location(29, "The Market", 30)
feds_farm_loc_3040.roads = {17: 5, 28: 7, 20: 10}
feds_farm_loc_4050 = Farm_Location(30, "Восточный барьер", 40)
feds_farm_loc_4050.roads = {21: 15, 28: 8, 17: 5}

trib_farm_loc_010 = Farm_Location(31, "Тренировочный центр", 0)
trib_farm_loc_010.roads = {15: 5, 32: 6, 33: 12}
trib_farm_loc_1020 = Farm_Location(32, "Проспект Справедливости", 10)
trib_farm_loc_1020.roads = {15: 5, 31: 6, 33: 10, 22: 10}
trib_farm_loc_2030 = Farm_Location(33, "Старая сеть метро", 20)
trib_farm_loc_2030.roads = {18: 10, 35: 8, 23: 15, 31: 12, 32: 10, 34: 7}
trib_farm_loc_3040 = Farm_Location(34, "Базар", 30)
trib_farm_loc_3040.roads = {18: 5, 33: 7, 22: 10}
trib_farm_loc_4050 = Farm_Location(35, "Окраинный компаунд", 40)
trib_farm_loc_4050.roads = {23: 15, 33: 8, 18: 5}

stai_farm_loc_010 = Farm_Location(36, "Район корпораций", 0)
stai_farm_loc_010.roads = {16: 5, 37: 6, 38: 12}
stai_farm_loc_1020 = Farm_Location(37, "Технотаун Север", 10)
stai_farm_loc_1020.roads = {16: 5, 36: 6, 38: 10, 24: 10}
stai_farm_loc_2030 = Farm_Location(38, "Транзитный узел", 20)
stai_farm_loc_2030.roads = {19: 10, 40: 8, 25: 15, 36: 12, 37: 10, 39: 7}
stai_farm_loc_3040 = Farm_Location(39, "Технотаун Юг", 30)
stai_farm_loc_3040.roads = {19: 5, 38: 7, 24: 10}
stai_farm_loc_4050 = Farm_Location(40, "Оружейный магазин", 40)
stai_farm_loc_4050.roads = {25: 15, 38: 8, 19: 5}
