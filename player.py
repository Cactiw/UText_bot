import math


class Player:

    stats = {}

    def __init__(self, id, username, nickname, sex, race, game_class):
        self.id = id
        self.username = username
        self.nickname = nickname


        self.sex = sex
        self.race = race
        self.game_class = game_class

        self.exp = 0
        self.lvl = 1
        self.free_points = 0
        self.fatigue = 0

        self.stats = {"endurance" : 5, "power" : 5, "armor" : 5, "mana_points" : 5,
                    "agility" : 5, }

        self.mana = self.stats["mana_points"] * 15
        self.hp = self.stats["endurance"] * 15

        self.location = 0

        self.resources = {"gold" : 0, "metal" : 0, "wood" : 0}

        self.on_character = {"head": None, "body": None, "shoulders": None, "legs": None, "feet": None,
                        "left_arm": None, "right_arm": None, "mount": None, }

        self.eq_backpack = {}
        self.al_backpack = {}
        self.res_backpack = {}

    def add_to_(self, list, item): # Добавление item в рюкзак list
        list.update([item.name, item.id])

    def lvl_up(self):
        self.lvl += 1
        self.stats["endurance"] += 1
        self.stats["power"] += 1
        self.stats["armor"] += 1
        self.stats["intelligence"] += 1
        self.stats["mana_points"] += 1
        self.stats["accuracy"] += 1
        self.stats["agility"] += 1
        if self.game_class == "Warrior":
            self.stats["power"] += 1
            self.stats["armor"] += 1
        elif self.game_class == "Mage" or self.game_class == "Cliric":
            self.stats["intelligence"] += 1
            self.stats["mana_points"] += 1
        elif self.game_class == "Archer":
            self.stats["accuracy"] += 1
            self.stats["agility"] += 1
        else:
            a = None
            # class name error

    def lvl_check(self):
        if self.exp >= int(((self.lvl + 1) ** 4) * math.log(self.lvl + 1, math.e)):
            self.lvl_up()

    def equip(self, equipment): # Надевание предмета
        if self.on_character[equipment.place] != None:
            self.add_to_(self.eq_backpack, equipment)
        self.on_character[equipment.place] = equipment.id

    def unequip(self, equipment): # Снятие предмета
        self.add_to_(self.eq_backpack, equipment)
        self.on_character[equipment.place] = None

    def change_location(self, location):
        a = None


