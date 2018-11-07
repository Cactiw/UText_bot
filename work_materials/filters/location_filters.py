from telegram.ext import BaseFilter
from work_materials.globals import dispatcher


class CapitalLocationFilter(BaseFilter):
    def filter(self, message):
        return dispatcher.user_data[message.from_user.id].get('status')\
               == "In Capital"


class GuildCastleLocationFilter(BaseFilter):
    def filter(self, message):
        return dispatcher.user_data[message.from_user.id].get('status')\
               == "In Guild Castle"


class TowerLocationFilter(BaseFilter):
    def filter(self, message):
        return dispatcher.user_data[message.from_user.id].get('status')\
               == "In Tower"


class FarmLocationFilter(BaseFilter):
    def filter(self, message):
        return dispatcher.user_data[message.from_user.id].get('status')\
               == "In Farm Location"


class ResourceLocationFilter(BaseFilter):
    def filter(self, message):
        return dispatcher.user_data[message.from_user.id].get('status')\
               == "In Resource Location"


class ResourceOffIslandLocationFilter(BaseFilter):
    def filter(self, message):
        return dispatcher.user_data[message.from_user.id].get('status')\
               == "In Resource Off Island Location"


class CastleLocationFilter(BaseFilter):
    def filter(self, message):
        return dispatcher.user_data[message.from_user.id].get('status')\
               == "In Castle"


class PortalLocationFilter(BaseFilter):
    def filter(self, message):
        return dispatcher.user_data[message.from_user.id].get('status')\
               == "In Portal Location"


class LocationFilter(BaseFilter):
    def filter(self, message):
        status = dispatcher.user_data[message.from_user.id].get('status')
        a = ["In Capital", "In Guild Castle", "In Tower", "In Farm Location", "In Resource Location",
             "In Resource Off Island Location", "In Castle", "In Portal Location"]
        return status in a  #Проверить работает или нет




capital_location_filter = CapitalLocationFilter()
guildCastle_location_filter = GuildCastleLocationFilter()
tower_location_filter = TowerLocationFilter()
farm_location_filter = FarmLocationFilter()
resource_location_filter = ResourceLocationFilter()
resource_offIsland_location_filter = ResourceOffIslandLocationFilter()
castle_location_filter = CastleLocationFilter()
portal_location_filter = PortalLocationFilter()
location_filter = LocationFilter()

