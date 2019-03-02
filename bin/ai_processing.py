from work_materials.globals import battle_with_bots_to_set, battles_need_treating, dispatcher
from bin.battle_processing import get_skill
import logging, traceback


def bots_processing():
    try:
        battle = battle_with_bots_to_set.get()
        while battle:
            try:
                #print("got ai battle")
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
                    #print(ai.aggro_list)
                    """for i in ai.aggro_list:
                        print("aggro list: ", i.participant.nickname in battle.dead_list, i.participant.nickname in battle.taunt_list, i.aggro)"""
                    ai.aggro_list.sort(key = lambda pib: (pib.participant.nickname not in battle.dead_list, pib.participant.nickname in battle.taunt_list, pib.aggro), reverse=True)
                    ai.skill = get_skill(ai.participant.game_class, "Атака")
                    targets = [ai.aggro_list[0].participant]
                    ai.targets = targets
                    battle.skills_queue.append(ai)
            except KeyboardInterrupt:
                return 0
            except Exception:
                for player_in_battle in battle.teams[0]:
                    try:
                        dispatcher.bot.send_message(chat_id = player_in_battle.participant.id, text = "<b>Ошибка при обработке ИИ</b>", parse_mode="HTML")
                    except Exception:
                        logging.error(traceback.format_exc())
                logging.error(traceback.format_exc())
            battles_need_treating.put(battle)
            battle = battle_with_bots_to_set.get()
    except KeyboardInterrupt:
        return 0
    except Exception:
        logging.error(traceback.format_exc())
