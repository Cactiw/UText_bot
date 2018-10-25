from telegram.ext import BaseFilter
from work_materials.globals import *



class Filter_Sex_Select(BaseFilter):
    def filter(self, message):
        return dispatcher.user_data[message.from_user.id].get('type') == 4

filter_sex_select= Filter_Sex_Select()


class Filter_Nickname_Select(BaseFilter):
    def filter(self, message):
        return dispatcher.user_data[message.from_user.id].get('type') == 5

filter_nickname_select= Filter_Nickname_Select()