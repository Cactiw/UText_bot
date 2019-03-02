from telegram.ext import BaseFilter
from work_materials.filters.location_filters import farm_location_filter
from work_materials.globals import dispatcher


class FarmFilter(BaseFilter):
    def filter(self, message):
        if message.text.find("Добывать") == 0:
            user_data = dispatcher.user_data.get(message.from_user.id)
            return user_data and user_data.get('status') == 'In Location' and farm_location_filter(message)
        return False

farm_filter = FarmFilter()