from libs.item import *
from libs.equipment import *
from bin.equipment_service import *


def get_item(type, id):
    item = None
    if type.find("e") == 0:
        item = get_equipment(id)
    return item

def get_item_and_list(type, id, player):
    item = None
    list = None
    if type.find("e") == 0:
        item = get_equipment(id)
        list = player.eq_backpack
    return [list, item]