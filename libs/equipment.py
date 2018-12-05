from libs.item import *
from work_materials.globals import conn, cursor

class Equipment(Item):

    def __init__(self, type, id, name,  place, endurance, power, armor, agility, charge):
        super(Equipment, self).__init__(type, id, name)

        self.place = place
        self.stats = {'endurance': endurance, 'power': power, 'armor': armor, 'speed': agility, 'charge': charge}


    def update_from_database(self):
        request = "SELECT type, name, endurance, power, armor, charge, speed FROM equipment WHERE id = '{0}'".format(self.id)
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
        self.stats.update({'charge' : row[5]})
        self.stats.update({'speed' : row[6]})
        return 0