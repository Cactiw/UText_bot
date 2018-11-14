from libs.item import *
from work_materials.globals import conn, cursor

class Equipment(Item):

    def __init__(self, type, id, name,  place, endurance, power, armor, agility):
        super(Equipment, self).__init__(type, id)

        self.name = name
        self.place = place
        self.stats = {'endurance': 0, 'power': 0, 'armor': 0, 'agility': 0, 'mana_points': 0}

    def update_from_database(self):
        request = "SELECT type, name, endurance, power, armor, agility FROM equipment WHERE id = '{0}'".format(self.id)
        print(request)
        cursor.execute(request)
        row = cursor.fetchone()
        if row is None:
            return None
        self.type = "e{0}".format(row[0])
        if row[0] == 'h':
            self.place = 'head'
        elif row[0] == 'b':
            self.place = 'body'
        elif row[0] == 's':
            self.place = 'shoulders'
        elif row[0] == 'l':
            self.place = 'left_arm'
        elif row[0] == 'r':
            self.place = 'right_arm'
        elif row[0] == 'z':
            self.place = 'legs'
        elif row[0] == 'f':
            self.place = 'feet'
        elif row[0] == 'm':
            self.place = 'mount'
        self.name = row[1]
        self.stats.update({'endurance' : row[2]})
        self.stats.update({'power' : row[3]})
        self.stats.update({'armor' : row[4]})
        self.stats.update({'agility' : row[5]})
        return 0