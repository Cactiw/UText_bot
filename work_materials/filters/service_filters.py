from work_materials.globals import *
from telegram.ext import BaseFilter


class Filter_Is_Admin(BaseFilter):
    def filter(self, message):
        return message.from_user.id in admin_id_list


class FilterBack(BaseFilter):
    def filter(self, message):
        return message.text == "Назад"


class MyFilterCommand(BaseFilter):
    def filter(self, message):
        return message.text[0] == '/'


filter_is_admin= Filter_Is_Admin()
filter_back = FilterBack()
filter_command = MyFilterCommand()