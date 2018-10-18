import math

class Equipment:

    def __init__(self, id, name,  place, endurance, power, armor, intelligence, accuracy, agility):
        self.id = id
        self.name = name
        self.place = place
        self.endurance = endurance
        self.power = power
        self.armor = armor
        self.intelligence = intelligence
        self.accuracy = accuracy
        self.agility = agility

class Player:

    sex = -1
    race = -1
    game_class = -1

    exp = 0
    lvl = 1
    free_points = 0
    fatigue = 0

    endurance = 5
    power = 5
    armor = 5
    intelligence = 5
    mana_points = 5
    accuracy = 5
    agility = 5

    mana = mana_points * 15
    hp = endurance * 15

    head = None
    body = None
    shoulders = None
    legs = None
    feet = None
    left_hand = None
    right_hand = None
    mount = None

    def set_character(self):
        print("in set_character\n")
        # get and set sex, race, game_class


    def __init__(self, id, username, nickname):
        self.id = id
        self.username = username
        self.nickname = nickname
        self.set_character()


    def lvl_up(self):
        self.lvl += 1
        self.endurance += 1
        self.power += 1
        self.armor += 1
        self.intelligence += 1
        self.mana_points += 1
        self.accuracy += 1
        self.agility += 1
        if self.game_class == "Warrior":
            self.power += 1
            self.armor += 1
        elif self.game_class == "Mage" or self.game_class == "Cliric":
            self.intelligence += 1
            self.mana_points += 1
        elif self.game_class == "Archer":
            self.accuracy += 1
            self.agility += 1


    def lvl_check(self):
        if self.exp >= int(((self.lvl + 1) ** 4) * math.log(self.lvl + 1, math.e)):
            self.lvl_up()


    def __add_points(self, place, equipment_id):
        if (place == None):
            return place
        else:
            place

    def equip(self, equipment):
        if (equipment.place == "head"):
            a = None
        elif (equipment.place == "body"):
            a = None
        elif (equipment.place == "shoulders"):
            a = None
        elif (equipment.place == "legs"):
            a = None
        elif (equipment.place == "feet"):
            a = None
        elif (equipment.place == "left hand"):
            a = None
        elif (equipment.place == "right hand"):
            a = None
        elif (equipment.place == "mount"):
            a = None