from telegram.ext import BaseFilter
from bin.player_service import get_player
from work_materials.globals import dispatcher

class CapitalLocationFilter(BaseFilter):
    def filter(self, message):
        location_id = get_player(message.from_user.id).location
        return location_id >= 14 and location_id <= 16


class FilterStartBattle(BaseFilter):
    def filter(self, message):
        return 'Битва' in message.text and capital_location_filter(message)


capital_location_filter = CapitalLocationFilter()
filter_start_battle = FilterStartBattle()


skills_for_enemies_names = ['Атака', 'Первый скилл', 'Третий скилл', 'Четвертый скилл']
skills_for_allies_names = ['Пятый скилл']
skills_for_anyone = ['Второй скилл']
skip_skill = ['Пропуск хода']


class FilterUseSkillOnEnemy(BaseFilter):
    def filter(self, message):
        return message.text in skills_for_enemies_names


class FilterUseSkillOnAlly(BaseFilter):
    def filter(self, message):
        return message.text in skills_for_allies_names


class FilterUseSkillOnAnyone(BaseFilter):
    def filter(self, message):
        return message.text in skills_for_anyone


class FilterStatusBattle(BaseFilter):
    def filter(self, message):
        return dispatcher.user_data.get(message.from_user.id).get('status') == 'Battle'


class FilterStatusChoosingTarget(BaseFilter):
    def filter(self, message):
        return dispatcher.user_data.get(message.from_user.id).get('status') == 'Choosing target'


class FilterBattleCancel(BaseFilter):
    def filter(self, message):
        return (dispatcher.user_data.get(message.from_user.id).get('status') == 'Choosing target' or
               dispatcher.user_data.get(message.from_user.id).get('status') == 'Battle waiting') and\
               message.text == 'Отмена'

class FilterBattleSkipTurn(BaseFilter):
    def filter(self, message):
        return message.text in skip_skill

filter_use_skill_on_enemy = FilterUseSkillOnEnemy()
filter_use_skill_on_ally = FilterUseSkillOnAlly()
filter_use_skill_on_anyone = FilterUseSkillOnAnyone()
filter_status_battle = FilterStatusBattle()
filter_status_choosing_target = FilterStatusChoosingTarget()
filter_battle_cancel = FilterBattleCancel()
filter_battle_skip_turn = FilterBattleSkipTurn()
