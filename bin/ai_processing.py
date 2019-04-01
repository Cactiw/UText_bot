from work_materials.globals import battle_with_bots_to_set, battles_need_treating, dispatcher, skills
from bin.battle_processing import get_skill
import logging, traceback


def bots_processing():
    try:
        battle = battle_with_bots_to_set.get()
        while battle:
            try:
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
                    #print(ai.aggro_list)
                    for i in ai.aggro_list:
                        print(battle.taunt_list)
                        print("aggro list: ", i.participant.nickname in list(battle.taunt_list.get(0)), i.aggro)
                    ai.aggro_list.sort(key = lambda pib: (pib.participant.nickname not in battle.dead_list,
                                                          battle.taunt_list.get(0).get(pib.participant.nickname) > 1 if
                                                          i.participant.nickname in list(battle.taunt_list.get(0)) else False,
                                                          pib.aggro), reverse=True)
                    ai.skill = None
                    skills_list = skills.get(ai.participant.game_class)
                    for skill_name in list(skills_list)[1:-1]:
                        print(skill_name, ai.participant.skill_cooldown)
                        skill_cooldown = ai.participant.skill_cooldown.get(skill_name)
                        if skill_cooldown == 0:
                            skill = skills_list.get(skill_name)
                            ai.skill = skill
                            break
                    if ai.skill is None:
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
            print("put from ai")
            battles_need_treating.put(battle)
            battle = battle_with_bots_to_set.get()
    except KeyboardInterrupt:
        return 0
    except Exception:
        logging.error(traceback.format_exc())
