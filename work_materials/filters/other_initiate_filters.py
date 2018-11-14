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

class Filter_Lvl_Up_Skill(BaseFilter):
    def filter(self, message):
        if dispatcher.user_data[message.from_user.id].get('status') == "Lvl_up_skill":
            a = ["1", "2", "3", "4", "5", "Готово"]
            for i in range(0, len(a)):
                if message.text == a[i]:
                    return 1
            return 0

filter_lvl_up_skill = Filter_Lvl_Up_Skill()

class Filter_Lvl_Up_Points(BaseFilter):
    def filter(self, message):
        if dispatcher.user_data[message.from_user.id].get('status') == "Lvl_up_points":
            a = ["Выносливость", "Броня", "Сила", "Ловкость", "Очки маны", "Готово"]
            for i in range(0, len(a)):
                if message.text == a[i]:
                    return 1
            return 0

filter_lvl_up_points = Filter_Lvl_Up_Points()