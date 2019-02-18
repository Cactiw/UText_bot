from libs.interprocess_dictionaty import InterprocessDictionary, interprocess_queue


class Skill:

    def __init__(self, name, format_string, type, priority, func):
        self.name = name
        self.format_string = format_string
        self.type = type
        self.priority = priority    #0 - для пропуска хода
        self.use_func = func

    def use_skill(self, targets, battle, player):
        self.use_func(targets, battle, player)


class BattleBuff:

    def __init__(self, buff = 0, turns = 0):
        self.turns = turns
        self.buff = buff

def skip_turn_func(targets, battle, player):
    pass


skip_turn_skill = Skill("Пропуск хода", "<b>{0}</b> пропустил ход", "buff", 0, skip_turn_func)


def attack_func(targets, battle, player):
    for i in targets:
        power = player.stats.get('power')
        curr_buffs = battle.buff_list.get(player.nickname).get('power')
        for j in curr_buffs:
            power += j.buff
        i.hp -= 5 * power

        if battle.damage_change.get(i.nickname) is None:
            battle.damage_change.update({i.nickname: {}})
        battle.damage_change.get(i.nickname).update({player.nickname: -5 * power})



attack_skill = Skill("Атака", "<b>{0}</b>  Атаковал  <b>{1}</b>", "damage", 10, attack_func)


#----------------------------------------------------------------------------------------------------


def operator_first_func(targets, battle, player):
    team = 0
    for i in battle.teams[1]:
        if i.participant.nickname == player.nickname:
            team = 1
    battle.taunt_list.get(team).update({player.nickname: 2 + 1})


def operator_second_func(targets, battle, player):
    for i in targets:
        battle.buff_list.get(i.nickname).get('power').append(BattleBuff(buff=2, turns=2 + 1))


def operator_third_func(targets, battle, player):
    for i in targets:
        power = player.stats.get('power')
        curr_buffs = battle.buff_list.get(player.nickname).get('power')
        for j in curr_buffs:
            power += j.buff
        i.hp -= 2 * power
        if battle.damage_change.get(i.nickname) is None:
            battle.damage_change.update({i.nickname: {}})
        battle.damage_change.get(i.nickname).update({player.nickname: -2 * power})


def operator_fourth_func(targets, battle, player):
    for i in targets:
        endurance = player.stats.get('endurance')
        curr_buffs = battle.buff_list.get(player.nickname).get('endurance')
        for j in curr_buffs:
            endurance += j.buff
        if i.hp + 20 <= endurance * 15:
            i.hp += 20
        else:
            i.hp = endurance * 15
        if battle.damage_change.get(i.nickname) is None:
            battle.damage_change.update({i.nickname: {}})
        battle.damage_change.get(i.nickname).update({player.nickname: 20})


def operator_fifth_func(targets, battle, player):
    for i in targets:
        interprocess_dict = InterprocessDictionary(i.id, "user_data", {'stunned': 1 + 1})
        interprocess_queue.put(interprocess_dict)
        battle.stun_list.update({i.nickname: 1 + 1})
        player.skill_cooldown.update({'Пятый навык': 3 + 1})


operator_first_skill = Skill("Первый навык", "<b>{0}</b>  использовал <b>Первый навык</b> на  <b>{1}</b>", "debuff", 1, operator_first_func)
operator_second_skill = Skill("Второй навык", "<b>{0}</b>  использовал <b>Второй навык</b> на  <b>{1}</b>", "buff", 5, operator_second_func)
operator_third_skill = Skill("Третий навык", "<b>{0}</b>  использовал <b>Третий навык</b> на  <b>{1}</b>", "damage", 6, operator_third_func)
operator_fourth_skill = Skill("Четвертый навык", "<b>{0}</b>  использовал <b>Четвертый навык</b> на  <b>{1}</b>", "buff", 2, operator_fourth_func)
operator_fifth_skill = Skill("Пятый навык", "<b>{0}</b>  использовал <b>Пятый навык</b> на  <b>{1}</b>", "debuff", 2, operator_fifth_func)


def hacker_first_func(targets, battle, player):
    for i in targets:
        battle.buff_list.get(i.nickname).get('power').append(BattleBuff(buff=-2, turns=2 + 1))


def hacker_second_func(targets, battle, player):
    for i in targets:
        battle.buff_list.get(i.nickname).get('power').append(BattleBuff(buff=2, turns=2 + 1))


def hacker_third_func(targets, battle, player):
    for i in targets:
        power = player.stats.get('power')
        curr_buffs = battle.buff_list.get(player.nickname).get('power')
        for j in curr_buffs:
            power += j.buff
        i.hp -= 2 * power
        if battle.damage_change.get(i.nickname) is None:
            battle.damage_change.update({i.nickname: {}})
        battle.damage_change.get(i.nickname).update({player.nickname: -2 * power})


def hacker_fourth_func(targets, battle, player):
    for i in targets:
        endurance = player.stats.get('endurance')
        curr_buffs = battle.buff_list.get(player.nickname).get('endurance')
        for j in curr_buffs:
            endurance += j.buff
        if i.hp + 20 <= endurance * 15:
            i.hp += 20
        else:
            i.hp = endurance * 15
        if battle.damage_change.get(i.nickname) is None:
            battle.damage_change.update({i.nickname: {}})
        battle.damage_change.get(i.nickname).update({player.nickname: 20})


def hacker_fifth_func(targets, battle, player):
    for i in targets:
        interprocess_dict = InterprocessDictionary(i.id, "user_data", {'stunned': 1 + 1})
        interprocess_queue.put(interprocess_dict)
        battle.stun_list.update({i.nickname: 1 + 1})
        player.skill_cooldown.update({'Пятый навык': 3 + 1})


hacker_first_skill = Skill("Первый навык", "<b>{0}</b>  использовал <b>Первый навык</b> на  <b>{1}</b>", "debuff", 1, hacker_first_func)
hacker_second_skill = Skill("Второй навык", "<b>{0}</b>  использовал <b>Второй навык</b> на  <b>{1}</b>", "buff", 7, hacker_second_func)
hacker_third_skill = Skill("Третий навык", "<b>{0}</b>  использовал <b>Третий навык</b> на  <b>{1}</b>", "damage", 7, hacker_third_func)
hacker_fourth_skill = Skill("Четвертый навык", "<b>{0}</b>  использовал <b>Четвертый навык</b> на  <b>{1}</b>", "buff", 3, hacker_fourth_func)
hacker_fifth_skill = Skill("Пятый навык", "<b>{0}</b>  использовал <b>Пятый навык</b> на  <b>{1}</b>", "debuff", 4, hacker_fifth_func)


def gunner_first_func(targets, battle, player):
    for i in targets:
        battle.buff_list.get(i.nickname).get('power').append(BattleBuff(buff=-2, turns=2 + 1))


def gunner_second_func(targets, battle, player):
    for i in targets:
        battle.buff_list.get(i.nickname).get('power').append(BattleBuff(buff=2, turns=2 + 1))


def gunner_third_func(targets, battle, player):
    for i in targets:
        power = player.stats.get('power')
        curr_buffs = battle.buff_list.get(player.nickname).get('power')
        for j in curr_buffs:
            power += j.buff
        i.hp -= 2 * power
        if battle.damage_change.get(i.nickname) is None:
            battle.damage_change.update({i.nickname: {}})
        battle.damage_change.get(i.nickname).update({player.nickname: -2 * power})


def gunner_fourth_func(targets, battle, player):
    for i in targets:
        endurance = player.stats.get('endurance')
        curr_buffs = battle.buff_list.get(player.nickname).get('endurance')
        for j in curr_buffs:
            endurance += j.buff
        if i.hp + 20 <= endurance * 15:
            i.hp += 20
        else:
            i.hp = endurance * 15
        if battle.damage_change.get(i.nickname) is None:
            battle.damage_change.update({i.nickname: {}})
        battle.damage_change.get(i.nickname).update({player.nickname: 20})


def gunner_fifth_func(targets, battle, player):
    for i in targets:
        interprocess_dict = InterprocessDictionary(i.id, "user_data", {'stunned': 1 + 1})
        interprocess_queue.put(interprocess_dict)
        battle.stun_list.update({i.nickname: 1 + 1})
        player.skill_cooldown.update({'Пятый навык': 3 + 1})


gunner_first_skill = Skill("Первый навык", "<b>{0}</b>  использовал <b>Первый навык</b> на  <b>{1}</b>", "debuff", 2, gunner_first_func)
gunner_second_skill = Skill("Второй навык", "<b>{0}</b>  использовал <b>Второй навык</b> на  <b>{1}</b>", "buff", 7, gunner_second_func)
gunner_third_skill = Skill("Третий навык", "<b>{0}</b>  использовал <b>Третий навык</b> на  <b>{1}</b>", "damage", 9, gunner_third_func)
gunner_fourth_skill = Skill("Четвертый навык", "<b>{0}</b>  использовал <b>Четвертый навык</b> на  <b>{1}</b>", "buff", 3, gunner_fourth_func)
gunner_fifth_skill = Skill("Пятый навык", "<b>{0}</b>  использовал <b>Пятый навык</b> на  <b>{1}</b>", "debuff", 1, gunner_fifth_func)


def biomechanic_first_func(targets, battle, player):
    for i in targets:
        battle.buff_list.get(i.nickname).get('power').append(BattleBuff(buff=-2, turns=2+1))



def biomechanic_second_func(targets, battle, player):
    for i in targets:
        battle.buff_list.get(i.nickname).get('power').append(BattleBuff(buff=2, turns=2 + 1))


def biomechanic_third_func(targets, battle, player):
    for i in targets:
        power = player.stats.get('power')
        curr_buffs = battle.buff_list.get(player.nickname).get('power')
        for j in curr_buffs:
            power += j.buff
        i.hp -= 2 * power
        if battle.damage_change.get(i.nickname) is None:
            battle.damage_change.update({i.nickname: {}})
        battle.damage_change.get(i.nickname).update({player.nickname: -2 * power})


def biomechanic_fourth_func(targets, battle, player):
    for i in targets:
        endurance = player.stats.get('endurance')
        curr_buffs = battle.buff_list.get(player.nickname).get('endurance')
        for j in curr_buffs:
            endurance += j.buff
        if i.hp + 20 <= endurance * 15:
            i.hp += 20
        else:
            i.hp = endurance * 15
        if battle.damage_change.get(i.nickname) is None:
            battle.damage_change.update({i.nickname: {}})
        battle.damage_change.get(i.nickname).update({player.nickname: 20})


def biomechanic_fifth_func(targets, battle, player):
    for i in targets:
        interprocess_dict = InterprocessDictionary(i.id, "user_data", {'stunned': 1 + 1})
        interprocess_queue.put(interprocess_dict)
        battle.stun_list.update({i.nickname: 1 + 1})
        player.skill_cooldown.update({'Пятый навык': 3 + 1})


biomechanic_first_skill = Skill("Первый навык", "<b>{0}</b>  использовал <b>Первый навык</b> на  <b>{1}</b>", "debuff", 2, biomechanic_first_func)
biomechanic_second_skill = Skill("Второй навык", "<b>{0}</b>  использовал <b>Второй навык</b> на  <b>{1}</b>", "buff", 6, biomechanic_second_func)
biomechanic_third_skill = Skill("Третий навык", "<b>{0}</b>  использовал <b>Третий навык</b> на  <b>{1}</b>", "damage", 5, biomechanic_third_func)
biomechanic_fourth_skill = Skill("Четвертый навык", "<b>{0}</b>  использовал <b>Четвертый навык</b> на  <b>{1}</b>", "buff", 2, biomechanic_fourth_func)
biomechanic_fifth_skill = Skill("Пятый навык", "<b>{0}</b>  использовал <b>Пятый навык</b> на  <b>{1}</b>", "debuff", 4, biomechanic_fifth_func)



