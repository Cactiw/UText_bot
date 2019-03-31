from libs.item import Item
from work_materials.globals import cursor


class Resource(Item):

    def __init__(self, type, id, name):

        super(Resource, self).__init__(type, id, name)

    def update_from_database(self):
        request = "select item_type, item_name from items where item_id = %s"
        cursor.execute(request, (self.id,))
        row = cursor.fetchone()
        self.type = row[0]
        self.name = row[1]
        return 0
