from libs.interprocess_dictionaty import InterprocessDictionary, interprocess_queue
import math


class Skill:

    def __init__(self, name, format_string, type, priority, func):
        self.name = name
        self.format_string = format_string
        self.type = type
        self.priority = priority    #0 - для пропуска хода
        self.use_func = func

    def use_skill(self, targets, battle, player):
        return self.use_func(targets, battle, player)


class BattleBuff:

    def __init__(self, buff = 0, turns = 0):
        self.turns = turns
        self.buff = buff

def skip_turn_func(targets, battle, player):       #Пропуск хода
    pass


skip_turn_skill = Skill("Пропуск хода", "•<b>{0}</b> пропустил ход {1}{2}\n", "buff", 0, skip_turn_func)


def attack_func(targets, battle, player):       #Обычная атака
    power = player.stats.get('power')
    armor = player.stats.get('armor')
    curr_buffs_power = battle.buff_list.get(player.nickname).get('power')
    for j in curr_buffs_power:
        power += j.buff
    curr_buffs_armor = battle.buff_list.get(player.nickname).get('armor')
    for j in curr_buffs_armor:
        armor += j.buff
    damage = power * 20 + power ** (4 / 5) * player.lvl ** (3 / 2)
    damage /= (1 - 0.052 * math.sqrt(armor - 5) / (0.9 + 0.048 * math.sqrt(armor - 5)))
    damage = int(damage)
    for i in targets:
        i.hp -= damage
    return str(-damage)




attack_skill = Skill("Атака", "•<b>{0}</b>  Атаковал  <b>{1}</b>  {2}\n", "damage", 10, attack_func)


#----------------------------------------------------------------------------------------------------

#Оператор - танк
def operator_first_func(targets, battle, player):   #Поднять щиты, только для себя
    team = 0
    for i in battle.teams[1]:
        if i.participant.nickname == player.nickname:
            team = 1
    battle.taunt_list.get(team).update({player.nickname: 2 + 1})
    return "🔰"


def operator_second_func(targets, battle, player):      #Бафф на атаку TODO разобаться - масс или таргет
    for i in targets:
        battle.buff_list.get(i.nickname).get('power').append(BattleBuff(buff=2, turns=2 + 1))
    return "+2 Сила"


def operator_third_func(targets, battle, player):   #Масс дамаг
    power = player.stats.get('power')
    for i in targets:
        curr_buffs = battle.buff_list.get(player.nickname).get('power')
        for j in curr_buffs:
            power += j.buff
        i.hp -= 2 * power
    return str(-2 * power)


def operator_fourth_func(targets, battle, player):      #Мощный удар + дебафф на броню
    for i in targets:
        endurance = player.stats.get('endurance')
        charge = player.stats.get('charge')
        curr_buffs_endurance = battle.buff_list.get(player.nickname).get('endurance')
        curr_buffs_charge = battle.buff_list.get(player.nickname).get('charge')
        for j in curr_buffs_endurance:
            endurance += j.buff
        for j in curr_buffs_charge:
            charge += j.buff
        heal = 4 * charge
        if i.hp + heal <= endurance * 25:
            i.hp += heal
            return str(heal)
        else:
            old_hp = i.hp
            i.hp = endurance * 25
            return str(i.hp - old_hp)


def operator_fifth_func(targets, battle, player):   #Стан
    for i in targets:
        interprocess_dict = InterprocessDictionary(i.id, "user_data", {'stunned': 1 + 1})
        interprocess_queue.put(interprocess_dict)
        battle.stun_list.update({i.nickname: 1 + 1})
        player.skill_cooldown.update({'Пятый навык': 3 + 1})
    return "💫"


operator_first_skill = Skill("Первый навык", "•<b>{0}</b>  использовал <b>Первый навык</b> на  <b>{1}</b>  {2}\n", "debuff", 1, operator_first_func)
operator_second_skill = Skill("Второй навык", "•<b>{0}</b>  использовал <b>Второй навык</b> на  <b>{1}</b>  {2}\n", "buff", 5, operator_second_func)
operator_third_skill = Skill("Третий навык", "•<b>{0}</b>  использовал <b>Третий навык</b> на  <b>{1}</b>  {2}\n", "damage", 6, operator_third_func)
operator_fourth_skill = Skill("Четвертый навык", "•<b>{0}</b>  использовал <b>Четвертый навык</b> на  <b>{1}</b>  {2}\n", "buff", 2, operator_fourth_func)
operator_fifth_skill = Skill("Пятый навык", "•<b>{0}</b>  использовал <b>Пятый навык</b> на  <b>{1}</b>  {2}\n", "debuff", 2, operator_fifth_func)

#Хакер - маг. урон
def hacker_first_func(targets, battle, player):  #Масс дамаг
    for i in targets:
        battle.buff_list.get(i.nickname).get('power').append(BattleBuff(buff=-2, turns=2 + 1))
    return "-2 power"


def hacker_second_func(targets, battle, player):  #Мощный дебаф на таргет
    for i in targets:
        battle.buff_list.get(i.nickname).get('power').append(BattleBuff(buff=2, turns=2 + 1))
    return "+2 power"


def hacker_third_func(targets, battle, player):  #Мощный удар + масс дебаф
    power = player.stats.get('power')
    for i in targets:
        curr_buffs = battle.buff_list.get(player.nickname).get('power')
        for j in curr_buffs:
            power += j.buffбафф
        i.hp -= 2 * power
    return str(-2 * power)


def hacker_fourth_func(targets, battle, player):   #баф на себя на ловкость, чтобы уклоняться от атак
    for i in targets:
        endurance = player.stats.get('endurance')
        charge = player.stats.get('charge')
        curr_buffs_endurance = battle.buff_list.get(player.nickname).get('endurance')
        curr_buffs_charge = battle.buff_list.get(player.nickname).get('charge')
        for j in curr_buffs_endurance:
            endurance += j.buff
        for j in curr_buffs_charge:
            charge += j.buff
        heal = 4 * charge
        if i.hp + heal <= endurance * 25:
            i.hp += heal
            return str(heal)
        else:
            old_hp = i.hp
            i.hp = endurance * 25
            return str(i.hp - old_hp)


def hacker_fifth_func(targets, battle, player):    #Масс дамаг + баф на команду
    for i in targets:
        interprocess_dict = InterprocessDictionary(i.id, "user_data", {'stunned': 1 + 1})
        interprocess_queue.put(interprocess_dict)
        battle.stun_list.update({i.nickname: 1 + 1})
        player.skill_cooldown.update({'Пятый навык': 3 + 1})
    return "💫"



hacker_first_skill = Skill("Первый навык", "•<b>{0}</b>  использовал <b>Первый навык</b> на  <b>{1}</b>  {2}\n", "debuff", 1, hacker_first_func)
hacker_second_skill = Skill("Второй навык", "•<b>{0}</b>  использовал <b>Второй навык</b> на  <b>{1}</b>  {2}\n", "buff", 7, hacker_second_func)
hacker_third_skill = Skill("Третий навык", "•<b>{0}</b>  использовал <b>Третий навык</b> на  <b>{1}</b>  {2}\n", "damage", 7, hacker_third_func)
hacker_fourth_skill = Skill("Четвертый навык", "•<b>{0}</b>  использовал <b>Четвертый навык</b> на  <b>{1}</b>  {2}\n", "buff", 3, hacker_fourth_func)
hacker_fifth_skill = Skill("Пятый навык", "•<b>{0}</b>  использовал <b>Пятый навык</b> на  <b>{1}</b>  {2}\n", "debuff", 4, hacker_fifth_func)

#Канонир - физ. урон
def gunner_first_func(targets, battle, player):     #Удар + бафф на себя на силу(?)
    for i in targets:
        battle.buff_list.get(i.nickname).get('power').append(BattleBuff(buff=-2, turns=2 + 1))
    return "-2 power"


def gunner_second_func(targets, battle, player):    #Масс дамаг + бафф на команду (слабее чем 5 скилл у хакера)
    for i in targets:
        battle.buff_list.get(i.nickname).get('power').append(BattleBuff(buff=2, turns=2 + 1))
    return "+2 power"


def gunner_third_func(targets, battle, player):     #Мощный бурст
    power = player.stats.get('power')
    for i in targets:
        curr_buffs = battle.buff_list.get(player.nickname).get('power')
        for j in curr_buffs:
            power += j.buff
        i.hp -= 2 * power
    return str(-2 * power)


def gunner_fourth_func(targets, battle, player):    #Мощный удар + дебафф на дамаг
    for i in targets:
        endurance = player.stats.get('endurance')
        charge = player.stats.get('charge')
        curr_buffs_endurance = battle.buff_list.get(player.nickname).get('endurance')
        curr_buffs_charge = battle.buff_list.get(player.nickname).get('charge')
        for j in curr_buffs_endurance:
            endurance += j.buff
        for j in curr_buffs_charge:
            charge += j.buff
        heal = 4 * charge
        if i.hp + heal <= endurance * 25:
            i.hp += heal
            return str(heal)
        else:
            old_hp = i.hp
            i.hp = endurance * 25
            return str(i.hp - old_hp)


def gunner_fifth_func(targets, battle, player):     #Удар + разоружение (считай стан)
    for i in targets:
        interprocess_dict = InterprocessDictionary(i.id, "user_data", {'stunned': 1 + 1})
        interprocess_queue.put(interprocess_dict)
        battle.stun_list.update({i.nickname: 1 + 1})
        player.skill_cooldown.update({'Пятый навык': 3 + 1})
    return "💫"


gunner_first_skill = Skill("Первый навык", "•<b>{0}</b>  использовал <b>Первый навык</b> на  <b>{1}</b>  {2}\n", "debuff", 2, gunner_first_func)
gunner_second_skill = Skill("Второй навык", "•<b>{0}</b>  использовал <b>Второй навык</b> на  <b>{1}</b>  {2}\n", "buff", 7, gunner_second_func)
gunner_third_skill = Skill("Третий навык", "•<b>{0}</b>  использовал <b>Третий навык</b> на  <b>{1}</b>  {2}\n", "damage", 9, gunner_third_func)
gunner_fourth_skill = Skill("Четвертый навык", "•<b>{0}</b>  использовал <b>Четвертый навык</b> на  <b>{1}</b>  {2}\n", "buff", 3, gunner_fourth_func)
gunner_fifth_skill = Skill("Пятый навык", "•<b>{0}</b>  использовал <b>Пятый навык</b> на  <b>{1}</b>  {2}\n", "debuff", 1, gunner_fifth_func)

#Биомеханик - хил
def biomechanic_first_func(targets, battle, player):    #Хилл
    for i in targets:
        battle.buff_list.get(i.nickname).get('power').append(BattleBuff(buff=-2, turns=2+1))
    return "-2 power"



def biomechanic_second_func(targets, battle, player):   #Диспел
    for i in targets:
        battle.buff_list.get(i.nickname).get('power').append(BattleBuff(buff=2, turns=2 + 1))
    return "+2 power"


def biomechanic_third_func(targets, battle, player):    #Масс дамаг (небольшой) + масс дебаф
    power = player.stats.get('power')
    for i in targets:
        curr_buffs = battle.buff_list.get(player.nickname).get('power')
        for j in curr_buffs:
            power += j.buff
        i.hp -= 2 * power
    return str(-2 * power)


def biomechanic_fourth_func(targets, battle, player):   #Масс хилл + масс дебаф
    for i in targets:
        endurance = player.stats.get('endurance')
        charge = player.stats.get('charge')
        curr_buffs_endurance = battle.buff_list.get(player.nickname).get('endurance')
        curr_buffs_charge = battle.buff_list.get(player.nickname).get('charge')
        for j in curr_buffs_endurance:
            endurance += j.buff
        for j in curr_buffs_charge:
            charge += j.buff
        heal = 4 * charge
        if i.hp + heal <= endurance * 25:
            i.hp += heal
            return str(heal)
        else:
            old_hp = i.hp
            i.hp = endurance * 25
            return str(i.hp - old_hp)


def biomechanic_fifth_func(targets, battle, player):    #Немота
    for i in targets:
        interprocess_dict = InterprocessDictionary(i.id, "user_data", {'stunned': 1 + 1})
        interprocess_queue.put(interprocess_dict)
        battle.stun_list.update({i.nickname: 1 + 1})
        player.skill_cooldown.update({'Пятый навык': 3 + 1})
    return "💫"


biomechanic_first_skill = Skill("Первый навык", "•<b>{0}</b>  использовал <b>Первый навык</b> на  <b>{1}</b>  {2}\n", "debuff", 2, biomechanic_first_func)
biomechanic_second_skill = Skill("Второй навык", "•<b>{0}</b>  использовал <b>Второй навык</b> на  <b>{1}</b>  {2}\n", "buff", 6, biomechanic_second_func)
biomechanic_third_skill = Skill("Третий навык", "•<b>{0}</b>  использовал <b>Третий навык</b> на  <b>{1}</b>  {2}\n", "damage", 5, biomechanic_third_func)
biomechanic_fourth_skill = Skill("Четвертый навык", "•<b>{0}</b>  использовал <b>Четвертый навык</b> на  <b>{1}</b>  {2}\n", "buff", 2, biomechanic_fourth_func)
biomechanic_fifth_skill = Skill("Пятый навык", "•<b>{0}</b>  использовал <b>Пятый навык</b> на  <b>{1}</b>  {2}\n", "debuff", 4, biomechanic_fifth_func)



