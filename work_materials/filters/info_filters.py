
from vk_bot import BaseFilter
from bin.player_service import *
from work_materials.globals import *
from work_materials.filters.service_filters import filter_back


class FilterInfo(BaseFilter):
    def filter(self, message):
        return message.text == 'Инфо'


class FilterInInfo(BaseFilter):
    def filter(self, message):
        return updater.dispatcher.user_data[message.from_user.id].get('status') == "Info"


class FilterBackpack(BaseFilter):
    def filter(self, message):
        return message.text == 'Рюкзак'

class FilterImplants(BaseFilter):
    def filter(self, message):
        return message.text == 'Импланты'


class FilterInfoReturn(BaseFilter):
    def filter(self, message):
        return filter_in_info(message) and filter_back(message)



filter_info = FilterInfo()
filter_in_info = FilterInInfo()
filter_print_backpack = FilterBackpack()
filter_implants = FilterImplants()
filter_info_return = FilterInfoReturn()
