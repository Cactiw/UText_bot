from telegram.ext import BaseFilter



class Filter_Human(BaseFilter):
    def filter(self, message):
        return 'Люди' in message.text

filter_human= Filter_Human()


class Filter_Orcs(BaseFilter):
    def filter(self, message):
        return 'Орки' in message.text

filter_orcs= Filter_Orcs()


class Filter_Elves(BaseFilter):
    def filter(self, message):
        return 'Эльфы' in message.text

filter_elves= Filter_Elves()



class Filter_Races(BaseFilter):
    def filter(self, message):
        return filter_human(message) or filter_orcs(message) or filter_elves(message)

filter_races = Filter_Races()