
from telegram.ext import BaseFilter
from bin.player_service import *
from work_materials.globals import *


class FilterInfo(BaseFilter):
    def filter(self, message):
        return message.text == 'Инфо'


class FilterInInfo(BaseFilter):
    def filter(self, message):
        return updater.dispatcher.user_data[message.from_user.id].get('status') == "Info"


class FilterBackpack(BaseFilter):
    def filter(self, message):
        return message.text == 'Рюкзак'



filter_info = FilterInfo()
filter_in_info = FilterInInfo()
filter_print_backpack = FilterBackpack()


def return_from_info(bot, update, user_data):
    player = get_player(update.message.from_user.id)
    update_status(user_data.get('saved_status'), player, user_data)
    show_general_buttons(bot, update, user_data)
