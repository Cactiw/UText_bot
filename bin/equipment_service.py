from libs.equipment import *

def get_equipment(id):
    equipment = Equipment(0, id, 0, 0, 0, 0, 0, 0, 0)
    equipment.update_from_database()
    return equipment
