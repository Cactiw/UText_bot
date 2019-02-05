from libs.interprocess_dictionaty import InterprocessDictionary, interprocess_queue

class Skill:

    def __init__(self, name, format_string, type, priority, func):
        self.name = name
        self.format_string = format_string
        self.type = type
        self.priority = priority    #0 - для пропуска хода
        self.use_func = func

    def use_skill(self, targets, battle):
        self.use_func(targets, battle)


def skip_turn_func(targets, battle):
    pass


skip_turn_skill = Skill("Пропуск хода", "<b>{0}</b> пропустил ход", "buff", 0, skip_turn_func)


def attack_func(targets, battle):
    for i in targets:
        i.hp -= 25


attack_skill = Skill("Атака", "<b>{0}</b>  Атаковал  <b>{1}</b> (-25)", "damage", 10, attack_func)


def operator_first_func(targets, battle):
    pass


def operator_second_func(targets, battle):
    pass


def operator_third_func(targets, battle):
    for i in targets:
        i.hp -= 10


def operator_fourth_func(targets, battle):
    for i in targets:
        if i.hp + 20 <= i.stats['endurance'] * 15:
            i.hp += 20
        else:
            i.hp = i.stats['endurance'] * 15


def operator_fifth_func(targets, battle):
    for i in targets:
        interprocess_dict = InterprocessDictionary(i.id, "user_data", {'stunned': 1})
        interprocess_queue.put(interprocess_dict)


operator_first_skill = Skill("Первый навык", "<b>{0}</b>  использовал <b>Первый навык</b> на  <b>{1}</b>\n", "buff", 1, operator_first_func)
operator_second_skill = Skill("Второй навык", "<b>{0}</b>  использовал <b>Второй навык</b> на  <b>{1}</b>\n", "damage", 5, operator_second_func)
operator_third_skill = Skill("Третий навык", "<b>{0}</b>  использовал <b>Третий навык</b> на  <b>{1}</b>\n", "damage", 6, operator_third_func)
operator_fourth_skill = Skill("Четвертый навык", "<b>{0}</b>  использовал <b>Четвертый навык</b> на  <b>{1}</b>\n", "buff", 2, operator_fourth_func)
operator_fifth_skill = Skill("Пятый навык", "<b>{0}</b>  использовал <b>Пятый навык</b> на  <b>{1}</b>\n", "buff", 2, operator_fifth_func)


def hacker_first_func(targets, battle):
    pass


def hacker_second_func(targets, battle):
    pass


def hacker_third_func(targets, battle):
    for i in targets:
        i.hp -= 10


def hacker_fourth_func(targets, battle):
    for i in targets:
        if i.hp + 20 <= i.stats['endurance'] * 15:
            i.hp += 20
        else:
            i.hp = i.stats['endurance'] * 15


def hacker_fifth_func(targets, battle):
    for i in targets:
        interprocess_dict = InterprocessDictionary(i.id, "user_data", {'stunned': 1})
        interprocess_queue.put(interprocess_dict)


hacker_first_skill = Skill("Первый навык", "<b>{0}</b>  использовал <b>Первый навык</b> на  <b>{1}</b>\n", "buff", 1, hacker_first_func)
hacker_second_skill = Skill("Второй навык", "<b>{0}</b>  использовал <b>Второй навык</b> на  <b>{1}</b>\n", "damage", 7, hacker_second_func)
hacker_third_skill = Skill("Третий навык", "<b>{0}</b>  использовал <b>Третий навык</b> на  <b>{1}</b>\n", "damage", 7, hacker_third_func)
hacker_fourth_skill = Skill("Четвертый навык", "<b>{0}</b>  использовал <b>Четвертый навык</b> на  <b>{1}</b>\n", "buff", 3, hacker_fourth_func)
hacker_fifth_skill = Skill("Пятый навык", "<b>{0}</b>  использовал <b>Пятый навык</b> на  <b>{1}</b>\n", "buff", 4, hacker_fifth_func)


def gunner_first_func(targets, battle):
    pass


def gunner_second_func(targets, battle):
    pass


def gunner_third_func(targets, battle):
    for i in targets:
        i.hp -= 10


def gunner_fourth_func(targets, battle):
    for i in targets:
        if i.hp + 20 <= i.stats['endurance'] * 15:
            i.hp += 20
        else:
            i.hp = i.stats['endurance'] * 15


def gunner_fifth_func(targets, battle):
    for i in targets:
        interprocess_dict = InterprocessDictionary(i.id, "user_data", {'stunned': 1})
        interprocess_queue.put(interprocess_dict)


gunner_first_skill = Skill("Первый навык", "<b>{0}</b>  использовал <b>Первый навык</b> на  <b>{1}</b>\n", "buff", 2, gunner_first_func)
gunner_second_skill = Skill("Второй навык", "<b>{0}</b>  использовал <b>Второй навык</b> на  <b>{1}</b>\n", "damage", 7, gunner_second_func)
gunner_third_skill = Skill("Третий навык", "<b>{0}</b>  использовал <b>Третий навык</b> на  <b>{1}</b>\n", "damage", 9, gunner_third_func)
gunner_fourth_skill = Skill("Четвертый навык", "<b>{0}</b>  использовал <b>Четвертый навык</b> на  <b>{1}</b>\n", "buff", 3, gunner_fourth_func)
gunner_fifth_skill = Skill("Пятый навык", "<b>{0}</b>  использовал <b>Пятый навык</b> на  <b>{1}</b>\n", "buff", 1, gunner_fifth_func)


def biomechanic_first_func(targets, battle):
    pass


def biomechanic_second_func(targets, battle):
    pass


def biomechanic_third_func(targets, battle):
    for i in targets:
        i.hp -= 10


def biomechanic_fourth_func(targets, battle):
    for i in targets:
        if i.hp + 20 <= i.stats['endurance'] * 15:
            i.hp += 20
        else:
            i.hp = i.stats['endurance'] * 15

def biomechanic_fifth_func(targets, battle):
    for i in targets:
        interprocess_dict = InterprocessDictionary(i.id, "user_data", {'stunned': 1})
        interprocess_queue.put(interprocess_dict)


biomechanic_first_skill = Skill("Первый навык", "<b>{0}</b>  использовал <b>Первый навык</b> на  <b>{1}</b>\n", "buff", 2, biomechanic_first_func)
biomechanic_second_skill = Skill("Второй навык", "<b>{0}</b>  использовал <b>Второй навык</b> на  <b>{1}</b>\n", "damage", 6, biomechanic_second_func)
biomechanic_third_skill = Skill("Третий навык", "<b>{0}</b>  использовал <b>Третий навык</b> на  <b>{1}</b>\n", "damage", 5, biomechanic_third_func)
biomechanic_fourth_skill = Skill("Четвертый навык", "<b>{0}</b>  использовал <b>Четвертый навык</b> на  <b>{1}</b>\n", "buff", 2, biomechanic_fourth_func)
biomechanic_fifth_skill = Skill("Пятый навык", "<b>{0}</b>  использовал <b>Пятый навык</b> на  <b>{1}</b>\n", "buff", 4, biomechanic_fifth_func)



