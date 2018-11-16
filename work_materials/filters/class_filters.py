from telegram.ext import BaseFilter
from work_materials.globals import *


class FilterOperator(BaseFilter):
    def filter(self, message):
        return 'Оператор' in message.text

filter_operator= FilterOperator()



class FilterCannonier(BaseFilter):
    def filter(self, message):
        return 'Канонир' in message.text

filter_cannonier= FilterCannonier()



class FilterHacker(BaseFilter):
    def filter(self, message):
        return 'Хакер' in message.text

filter_hacker= FilterHacker()



class FilterBiomechanic(BaseFilter):
    def filter(self, message):
        return 'Биомеханик' in message.text

filter_biomechanic= FilterBiomechanic()



class Filter_Classes(BaseFilter):
    def filter(self, message):
        return (filter_operator(message) or filter_cannonier(message) or filter_hacker(message) or filter_biomechanic(message)) and \
               dispatcher.user_data[message.from_user.id].get('type') == 3

filter_classes = Filter_Classes()