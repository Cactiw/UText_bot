from telegram.ext import BaseFilter
from bin.player_service import get_player

class CapitalLocationFilter(BaseFilter):
    def filter(self, message):
        location_id = get_player(message.from_user.id).location
        return location_id >= 14 and location_id <= 16


capital_location_filter = CapitalLocationFilter()


class Filter_Create_Lot(BaseFilter):
    def filter(self, message):
        return "/create_lot" in message.text and capital_location_filter(message)


class Filter_Cancel_Lot(BaseFilter):
    def filter(self, message):
        return "/cancel_lot" in message.text and capital_location_filter(message)


class Filter_Bet(BaseFilter):
    def filter(self, message):
        return "/bet" in message.text and capital_location_filter(message)

class Filter_Lots(BaseFilter):
    def filter(self, message):
        return "/lots" in message.text and capital_location_filter(message)


filter_create_lot = Filter_Create_Lot()
filter_cancel_lot = Filter_Cancel_Lot()
filter_bet = Filter_Bet()
filter_lots = Filter_Lots()
