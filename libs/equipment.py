from libs.item import *
from work_materials.globals import conn, cursor

class Equipment(Item):

    def __init__(self, type, id, name,  place, endurance, power, armor, intelligence, accuracy, agility):
        super(Equipment, self).__init__(type, id)

        self.name = name
        self.place = place
        self.stats = {'endurance': 0, 'power': 0, 'armor': 0, 'agility': 0, 'mana_points': 0}

    def update_from_database(self):
        request = "SELECT type, name, endurance, power, armor, intelligence, accuracy, agility FROM equipment WHERE id = '{0}'".format(self.id)
        cursor.execute(request)
        row = cursor.fetchone()
        if row is None:
            return None
        self.type = "e{0}".format(row[0])
        self.name = row[1]
        self.endurance = row[2]
        self.power = row[3]
        self.armor = row[4]
        self.intelligence = row[5]
        self.accuracy = row[6]
        self.agility = row[7]
        return 0