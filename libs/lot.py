import datetime
import pytz
from work_materials.globals import cursor, conn

class Lot:

    def __init__(self, item, player_created, price, buyout_price, duration):
        self.item = item
        self.player_created = player_created
        self.price = price
        self.buyout_price = buyout_price
        self.duration = duration

    def create(self):
        self.time_start = datetime.datetime.now(tz = pytz.timezone('Europe/Moscow'))
        self.time_end = self.time_start + datetime.timedelta(hours=self.duration)
        item_id = self.item.id
        item_type = self.item.type

        request = "insert into lots(item_type, item_id, item_name, player_created_id," \
                  " price, buyout_price, time_start, time_end) " \
                  "values('{0}', '{1}', '{2}', '{3}'," \
                  " '{4}', '{5}', '{6}', '{7}') returning lot_id".format(item_type, item_id, self.item.name, self.player_created.id,
                                                 self.price, self.buyout_price, self.time_start, self.time_end)
        cursor.execute(request)
        conn.commit()
        id = cursor.fetchone()[0]
        return id
