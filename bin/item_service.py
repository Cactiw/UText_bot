from libs.item import *
from libs.equipment import *
from libs.resource import Resource
from work_materials.globals import cursor


def get_equipment(id):
    equipment = Equipment(0, id, 0, 0, 0, 0, 0, 0, 0)
    equipment.update_from_database()
    return equipment


def get_resource(id):
    resource = Resource(None, id, None)
    resource.update_from_database()
    return resource


def get_resource_by_rarity(rarity):
    request = "select item_id, item_name, item_type from items where item_rarity = %s order by random() limit 1"
    cursor.execute(request, (rarity,))
    row = cursor.fetchone()
    if row is None:
        return None
    return Resource(row[0], row[1], row[2], rarity)


def get_item(type, id):
    item = None
    if type.find("e") == 0:
        item = get_equipment(id)
    if type.find("r") == 0:
        item = get_resource(id)
    return item


def get_item_and_list(type, id, player):
    item = None
    list = None
    if type.find("e") == 0:
        item = get_equipment(id)
        list = player.eq_backpack
    elif type.find("r") == 0:
        item = get_item(type, id)
        list = player.res_backpack
    return [list, item]
