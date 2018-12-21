from telegram.ext import BaseFilter
from work_materials.globals import *
from bin.player_service import get_player



class CapitalLocationFilter(BaseFilter):
    def filter(self, message):
        location_id = get_player(message.from_user.id).location
        return location_id >= 14 and location_id <= 16


capital_location_filter = CapitalLocationFilter()


class FilterStartBattle(BaseFilter):
    def filter(self, message):
        return 'Битва' in message.text and capital_location_filter(message)

filter_start_battle = FilterStartBattle()