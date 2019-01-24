from telegram.ext import BaseFilter


class FilterGroupKick(BaseFilter):
    def filter(self, message):
        return message.text.find("/group_kick_") == 0

group_kick_filter = FilterGroupKick()
