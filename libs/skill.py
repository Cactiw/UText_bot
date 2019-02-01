

class Skill:

    def __init__(self, name, format_string, type, priority, func):
        self.name = name
        self.format_string = format_string
        self.type = type
        self.priority = priority    #0 - для пропуска хода
        self.use_func = func

    def use_skill(self, args):
        self.use_func(args)


def skip_turn_func(target):
    pass


skip_turn_skill = Skill("Пропуск хода", "<b>{0}</b>  пропустил ход", "buff", 0, skip_turn_func)


def attack_func(target):
    target.hp -= 25


attack_skill = Skill("Атака", "<b>{0}</b>  Атаковал  <b>{1}</b> (-25)", "damage", 10, attack_func)


def operator_first_func(target):
    pass


def operator_second_func(target):
    pass


def operator_third_func(target):
    pass


def operator_fourth_func(target):
    pass


def operator_fifth_func(target):
    pass


operator_first_skill = Skill("Первый навык", "<b>{0}</b>  использовал <b>Первый навык</b> на  <b>{1}</b>", "buff", 1, operator_first_func)
operator_second_skill = Skill("Второй навык", "<b>{0}</b>  использовал <b>Второй навык</b> на  <b>{1}</b>", "damage", 5, operator_first_func)
operator_third_skill = Skill("Третий навык", "<b>{0}</b>  использовал <b>Третий навык</b> на  <b>{1}</b>", "damage", 6, operator_first_func)
operator_fourth_skill = Skill("Четвертый навык", "<b>{0}</b>  использовал <b>Четвертый навык</b> на  <b>{1}</b>", "buff", 2, operator_first_func)
operator_fifth_skill = Skill("Пятый навык", "<b>{0}</b>  использовал <b>Пятый навык</b> на  <b>{1}</b>", "buff", 2, operator_first_func)


def hacker_first_func(target):
    pass


def hacker_second_func(target):
    pass


def hacker_third_func(target):
    pass


def hacker_fourth_func(target):
    pass


def hacker_fifth_func(target):
    pass


hacker_first_skill = Skill("Первый навык", "<b>{0}</b>  использовал <b>Первый навык</b> на  <b>{1}</b>", "buff", 1, hacker_first_func)
hacker_second_skill = Skill("Второй навык", "<b>{0}</b>  использовал <b>Второй навык</b> на  <b>{1}</b>", "damage", 7, hacker_first_func)
hacker_third_skill = Skill("Третий навык", "<b>{0}</b>  использовал <b>Третий навык</b> на  <b>{1}</b>", "damage", 7, hacker_first_func)
hacker_fourth_skill = Skill("Четвертый навык", "<b>{0}</b>  использовал <b>Четвертый навык</b> на  <b>{1}</b>", "buff", 3, hacker_first_func)
hacker_fifth_skill = Skill("Пятый навык", "<b>{0}</b>  использовал <b>Пятый навык</b> на  <b>{1}</b>", "buff", 4, hacker_first_func)


def gunner_first_func(target):
    pass


def gunner_second_func(target):
    pass


def gunner_third_func(target):
    pass


def gunner_fourth_func(target):
    pass


def gunner_fifth_func(target):
    pass


gunner_first_skill = Skill("Первый навык", "<b>{0}</b>  использовал <b>Первый навык</b> на  <b>{1}</b>", "buff", 2, gunner_first_func)
gunner_second_skill = Skill("Второй навык", "<b>{0}</b>  использовал <b>Второй навык</b> на  <b>{1}</b>", "damage", 7, gunner_first_func)
gunner_third_skill = Skill("Третий навык", "<b>{0}</b>  использовал <b>Третий навык</b> на  <b>{1}</b>", "damage", 9, gunner_first_func)
gunner_fourth_skill = Skill("Четвертый навык", "<b>{0}</b>  использовал <b>Четвертый навык</b> на  <b>{1}</b>", "buff", 3, gunner_first_func)
gunner_fifth_skill = Skill("Пятый навык", "<b>{0}</b>  использовал <b>Пятый навык</b> на  <b>{1}</b>", "buff", 1, gunner_first_func)


def biomechanic_first_func(target):
    pass


def biomechanic_second_func(target):
    pass


def biomechanic_third_func(target):
    pass


def biomechanic_fourth_func(target):
    pass


def biomechanic_fifth_func(target):
    pass


biomechanic_first_skill = Skill("Первый навык", "<b>{0}</b>  использовал <b>Первый навык</b> на  <b>{1}</b>", "buff", 2, biomechanic_first_func)
biomechanic_second_skill = Skill("Второй навык", "<b>{0}</b>  использовал <b>Второй навык</b> на  <b>{1}</b>", "damage", 6, biomechanic_first_func)
biomechanic_third_skill = Skill("Третий навык", "<b>{0}</b>  использовал <b>Третий навык</b> на  <b>{1}</b>", "damage", 5, biomechanic_first_func)
biomechanic_fourth_skill = Skill("Четвертый навык", "<b>{0}</b>  использовал <b>Четвертый навык</b> на  <b>{1}</b>", "buff", 2, biomechanic_first_func)
biomechanic_fifth_skill = Skill("Пятый навык", "<b>{0}</b>  использовал <b>Пятый навык</b> на  <b>{1}</b>", "buff", 4, biomechanic_first_func)



