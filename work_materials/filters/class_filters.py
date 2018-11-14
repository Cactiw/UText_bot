from telegram.ext import BaseFilter
from work_materials.globals import *




class Filter_Warrior(BaseFilter):
    def filter(self, message):
        return 'Воин' in message.text

filter_warrior= Filter_Warrior()



class Filter_Mage(BaseFilter):
    def filter(self, message):
        return 'Маг' in message.text

filter_mage= Filter_Mage()



class Filter_Archer(BaseFilter):
    def filter(self, message):
        return 'Лучник' in message.text

filter_archer= Filter_Archer()



class Filter_Cleric(BaseFilter):
    def filter(self, message):
        return 'Клирик' in message.text

filter_cleric= Filter_Cleric()



class Filter_Classes(BaseFilter):
    def filter(self, message):
        return (filter_warrior(message) or filter_mage(message) or filter_archer(message) or filter_cleric(message)) and \
               dispatcher.user_data[message.from_user.id].get('type') == 3

filter_classes = Filter_Classes()