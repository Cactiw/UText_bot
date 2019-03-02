from work_materials.globals import battle_with_bots_to_set, battles_need_treating, dispatcher
from bin.battle_processing import get_skill


def bots_processing():
    battle = battle_with_bots_to_set.get()
    while battle:
        print("got ai battle")
        aggro_list = battle.aggro_list
        if not aggro_list:
            #   Заполнение агро-листа в первый раз
            for ai in battle.teams[1]:
                current_ai_aggro_list = []
                for player in battle.teams[0]:
                    current_ai_aggro_list.append(player)
                aggro_list.update({ai.participant.nickname : current_ai_aggro_list})
                ai.aggro_list = current_ai_aggro_list
        for ai in battle.teams[1]:
            print(ai.aggro_list)
            ai.aggro_list.sort(key = lambda pib:pib.aggro)
            ai.skill = get_skill(ai.participant.game_class, "Атака")
            targets = [ai.aggro_list[0].participant]
            ai.targets = targets
            battle.skills_queue.append(ai)
        battles_need_treating.put(battle)
        battle = battle_with_bots_to_set.get()
