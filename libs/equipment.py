from libs.item import *

class Equipment(Item):

    def __init__(self, type, id, name,  place, endurance, power, armor, intelligence, accuracy, agility):
        super(Equipment, self).__init__(type, id)

        self.name = name
        self.place = place
        self.stats = {'endurance': 0, 'power': 0, 'armor': 0, 'agility': 0, 'mana_points': 0}
