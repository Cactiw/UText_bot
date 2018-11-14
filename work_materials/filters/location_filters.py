from telegram.ext import BaseFilter
from work_materials.globals import *


class CapitalLocationFilter(BaseFilter):
    def filter(self, message):
        location_id = players.get(message.from_user.id).location
        return location_id >= 14 and location_id <= 16 and dispatcher.user_data[message.from_user.id].get(
            'status') == 'In Location'


class GuildCastleLocationFilter(BaseFilter):
    def filter(self, message):
        location_id = players.get(message.from_user.id).location
        return location_id >= 17 and location_id <= 19 and dispatcher.user_data[message.from_user.id].get('status') == 'In Location'


class TowerLocationFilter(BaseFilter):
    def filter(self, message):
        location_id = players.get(message.from_user.id).location
        return location_id >= 5 and location_id <= 10 and dispatcher.user_data[message.from_user.id].get('status') == 'In Location'


class FarmLocationFilter(BaseFilter):
    def filter(self, message):
        location_id = players.get(message.from_user.id).location
        return location_id >= 26 and location_id <= 40 and dispatcher.user_data[message.from_user.id].get('status') == 'In Location'


class ResourceLocationFilter(BaseFilter):
    def filter(self, message):
        location_id = players.get(message.from_user.id).location
        return location_id >= 20 and location_id <= 25 and dispatcher.user_data[message.from_user.id].get('status') == 'In Location'


class ResourceOffIslandLocationFilter(BaseFilter):
    def filter(self, message):
        location_id = players.get(message.from_user.id).location
        return location_id >= 11 and location_id <= 13 and dispatcher.user_data[message.from_user.id].get('status') == 'In Location'


class CastleLocationFilter(BaseFilter):
    def filter(self, message):
        location_id = players.get(message.from_user.id).location
        return location_id >= 2 and location_id <= 4 and dispatcher.user_data[message.from_user.id].get('status') == 'In Location'


class PortalLocationFilter(BaseFilter):
    def filter(self, message):
        location_id = players.get(message.from_user.id).location
        return location_id == 1 and dispatcher.user_data[message.from_user.id].get('status') == 'In Location'


class LocationFilter(BaseFilter):
    def filter(self, message):
        return dispatcher.user_data[message.from_user.id].get('status') == 'In Location'


class TravelFilter(BaseFilter):
    def filter(self, message):
        #print(message.text)
        return message.text == 'Отправиться'


class ChoosingWayFilter(BaseFilter):
    def filter(self, message):
        return dispatcher.user_data[message.from_user.id].get('status') == 'Choosing way'


class FastTravel(BaseFilter):
    def filter(self, message):
        return dispatcher.user_data[message.from_user.id].get('status') == 'Traveling'

capital_location_filter = CapitalLocationFilter()
guildCastle_location_filter = GuildCastleLocationFilter()
tower_location_filter = TowerLocationFilter()
farm_location_filter = FarmLocationFilter()
resource_location_filter = ResourceLocationFilter()
resource_offIsland_location_filter = ResourceOffIslandLocationFilter()
castle_location_filter = CastleLocationFilter()
portal_location_filter = PortalLocationFilter()
location_filter = LocationFilter()
travel_filter = TravelFilter()
choosing_way_filter = ChoosingWayFilter()
fast_travel_filter = FastTravel()

