from telegram.ext import BaseFilter
from work_materials.globals import *
from work_materials.filters.location_filters import capital_location_filter

class Filter_Merchant(BaseFilter):
    def filter(self, message):
        return message.text == 'Торговец' and dispatcher.user_data[message.from_user.id].get('status') == 'In Location' and capital_location_filter(message)



class Filter_Merchant_Weapon(BaseFilter):
    def filter(self, message):
        return message.text == 'Оружие' and dispatcher.user_data[message.from_user.id].get('status') == 'Merchant'


class Filter_Merchant_Head(BaseFilter):
    def filter(self, message):
        return message.text == 'Голова' and dispatcher.user_data[message.from_user.id].get('status') == 'Merchant'


class Filter_Merchant_Body(BaseFilter):
    def filter(self, message):
        return message.text == 'Тело' and dispatcher.user_data[message.from_user.id].get('status') == 'Merchant'


class Filter_Merchant_Gloves(BaseFilter):
    def filter(self, message):
        return message.text == 'Перчатки' and dispatcher.user_data[message.from_user.id].get('status') == 'Merchant'


class Filter_Merchant_Legs(BaseFilter):
    def filter(self, message):
        return message.text == 'Ноги' and dispatcher.user_data[message.from_user.id].get('status') == 'Merchant'


class Filter_Merchant_Boots(BaseFilter):
    def filter(self, message):
        return message.text == 'Ботинки' and dispatcher.user_data[message.from_user.id].get('status') == 'Merchant'


class Filter_Merchant_Mounts(BaseFilter):
    def filter(self, message):
        return message.text == 'Средства передвижения' and dispatcher.user_data[message.from_user.id].get('status') == 'Merchant'


class Filter_Merchant_Implants(BaseFilter):
    def filter(self, message):
        return message.text == 'Импланты' and dispatcher.user_data[message.from_user.id].get('status') == 'Merchant'


class Filter_Merchant_Sell(BaseFilter):
    def filter(self, message):
        return message.text == 'Продать' and dispatcher.user_data[message.from_user.id].get('status') == 'Merchant'


filter_merchant = Filter_Merchant()

filter_merchant_weapon = Filter_Merchant_Weapon()
filter_merchant_head = Filter_Merchant_Head()
filter_merchant_body = Filter_Merchant_Body()
filter_merchant_gloves = Filter_Merchant_Gloves()
filter_merchant_legs = Filter_Merchant_Legs()
filter_merchant_boots = Filter_Merchant_Boots()
filter_merchant_mounts = Filter_Merchant_Mounts()
filter_merchant_implants = Filter_Merchant_Implants()
filter_merchant_sell = Filter_Merchant_Sell()

class Filter_Merchant_Buy(BaseFilter):
    def filter(self, message):
        return filter_merchant_head(message) or filter_merchant_body(message) or filter_merchant_gloves(message) or \
               filter_merchant_legs(message) or filter_merchant_boots(message) or filter_merchant_mounts(message) or filter_merchant_implants(message)

filter_merchant_buy = Filter_Merchant_Buy()


class Filter_Return_From_Merchant(BaseFilter):
    def filter(self, message):
        return message.text == 'Назад' and dispatcher.user_data[message.from_user.id].get('status') == 'Merchant'



class Filter_Buy_Equipment(BaseFilter):
    def filter(self, message):
        return ('/buy' in message.text) and dispatcher.user_data[message.from_user.id].get('status') == 'Merchant'


filter_return_from_merchant = Filter_Return_From_Merchant()
filter_buy_equipment = Filter_Buy_Equipment()