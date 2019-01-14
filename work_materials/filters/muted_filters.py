from telegram.ext import BaseFilter
from work_materials.globals import *


class FilterPlayerMuted(BaseFilter):
    def filter(self, message):
        return message.from_user.id in muted_players

filter_player_muted = FilterPlayerMuted()