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


skills_for_enemies_names = ['Атака', 'Пятый навык']
skills_for_allies_names = ['Второй навык']
skills_for_anyone = ['Четвертый навык']
skip_skill = ['Пропуск хода']
skills_on_enemy_team = ['Третий навык', 'Первый навык']
skills_on_ally_team = []


class FilterUseSkillOnEnemy(BaseFilter):
    def filter(self, message):
        return message.text in skills_for_enemies_names


class FilterUseSkillOnEnemyTeam(BaseFilter):
    def filter(self, message):
        return message.text in skills_on_enemy_team


class FilterUseSkillOnAlly(BaseFilter):
    def filter(self, message):
        return message.text in skills_for_allies_names


class FilterUseSkillOnAllyTeam(BaseFilter):
    def filter(self, message):
        return message.text in skills_on_ally_team


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


class FilterBattleWaitingUpdate(BaseFilter):
    def filter(self, message):
        return dispatcher.user_data.get(message.from_user.id).get('Battle waiting update') == 1


class FilterBattleDead(BaseFilter):
    def filter(self, message):
        return dispatcher.user_data.get(message.from_user.id).get('status') == "Battle_dead"


filter_use_skill_on_enemy = FilterUseSkillOnEnemy()
filter_use_skill_on_ally = FilterUseSkillOnAlly()
filter_use_skill_on_anyone = FilterUseSkillOnAnyone()
filter_status_battle = FilterStatusBattle()
filter_status_choosing_target = FilterStatusChoosingTarget()
filter_battle_cancel = FilterBattleCancel()
filter_battle_skip_turn = FilterBattleSkipTurn()
filter_battle_waiting_update = FilterBattleWaitingUpdate()
filter_battle_dead = FilterBattleDead()
filter_use_skill_on_enemy_team = FilterUseSkillOnEnemyTeam()
filter_use_skill_on_ally_team = FilterUseSkillOnAllyTeam()
