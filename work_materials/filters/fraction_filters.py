from telegram.ext import BaseFilter
from work_materials.globals import *


class FilterFeds(BaseFilter):
    def filter(self, message):
        return 'Федералы' in message.text


class FilterStai(BaseFilter):
    def filter(self, message):
        return 'Стая' in message.text


class FilterTrib(BaseFilter):
    def filter(self, message):
        return 'Трибунал' in message.text


class FilterFractions(BaseFilter):
    def filter(self, message):
        return (filter_feds(message) or filter_stai(message) or filter_trib(message)) and \
               dispatcher.user_data[message.from_user.id].get('type') == 1


class FilterHuman(BaseFilter):
    def filter(self, message):
        return message.text == 'Человек'


class FilterApparatus(BaseFilter):
    def filter(self, message):
        return message.text == 'Аппарат'


class FilterRace(BaseFilter):
    def filter(self, message):
        return (filter_human(message) or filter_apparatus(message))and \
                dispatcher.user_data[message.from_user.id].get('type') == 2


filter_stai= FilterStai()
filter_feds= FilterFeds()
filter_trib= FilterTrib()
filter_fractions = FilterFractions()
filter_human = FilterHuman()
filter_apparatus = FilterApparatus()
filter_race = FilterRace()
