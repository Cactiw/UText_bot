from vk_bot import BaseFilter


class Filter_Equip(BaseFilter):
    def filter(self, message):
        return "/equip_" in message.text


class Filter_Unequip(BaseFilter):
    def filter(self, message):
        return "/unequip_" in message.text

filter_equip = Filter_Equip()
filter_unequip = Filter_Unequip()