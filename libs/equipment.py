from libs.item import *

class Equipment(Item):

    def __init__(self, type, id, name,  place, endurance, power, armor, intelligence, accuracy, agility):
        super(Equipment, self).__init__(type, id)
        self.name = name
        self.place = place
        self.endurance = endurance
        self.power = power
        self.armor = armor
        self.intelligence = intelligence
        self.accuracy = accuracy
        self.agility = agility
