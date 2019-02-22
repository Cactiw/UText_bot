from work_materials.globals import *
from telegram.ext import BaseFilter
from work_materials.ban_list import ban_ids, white_list

class Filter_Is_Admin(BaseFilter):
    def filter(self, message):
        return message.from_user.id in admin_id_list


class FilterIsNotAdmin(BaseFilter):
    def filter(self, message):
        return message.from_user.id not in admin_id_list


class FilterBack(BaseFilter):
    def filter(self, message):
        return message.text == "Назад"


class MyFilterCommand(BaseFilter):
    def filter(self, message):
        return message.text[0] == '/'

class FilterIsBanned(BaseFilter):
    def filter(self, message):
        return message.from_user.id in ban_ids

class FilterInWhiteList(BaseFilter):
    def filter(self, message):
        return message.from_user.id in white_list


filter_is_admin= Filter_Is_Admin()
filter_back = FilterBack()
filter_command = MyFilterCommand()
filter_is_not_admin = FilterIsNotAdmin()
filter_is_banned = FilterIsBanned()
filter_in_white_list = FilterInWhiteList()