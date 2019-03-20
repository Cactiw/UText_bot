from random import randint
from libs.skill import Skill, attack_func, BattleBuff


class Enemy:
    def __init__(self, id, name, lvl):
        self.id = id
        self.name = name
        self.lvl = lvl
        self.game_class = "AI"
        self.is_ai = True
        self.aggro_list = None


class AIDSEnemy(Enemy):
    def __init__(self, lvl):
        super(AIDSEnemy, self).__init__(1, "AIDS", lvl)
        self.nickname = "AIDS"
        self.game_class = "AI_AIDSEnemy"

        self.stats = {'endurance': 20, 'power': 5, 'armor': 5, 'charge': 5, 'speed': 5}
        for i in range(lvl):
            j = randint(1, 5)
            if j == 1:
                self.stats['endurance'] += 1
            elif j == 2:
                self.stats['power'] += 1
            elif j == 3:
                self.stats['armor'] += 1
            elif j == 4:
                self.stats['charge'] += 1
            else:
                self.stats['speed'] += 1

        self.skill_cooldown = {}

        self.skill_names = ['Blood atack', 'Ass atack']

        self.charge = self.stats['charge'] * 13
        self.hp = self.stats['endurance'] * 13
        self.update_cooldown()
        #self.damage_taken_by_armor = 0

    def update_cooldown(self):
        from work_materials.globals import skills
        class_skills = skills.get(self.game_class)
        for i in list(class_skills.values()):
            if i.name == 'Атака' or i.name == 'Пропуск хода':
                continue
            self.skill_cooldown.update({i.name: 0})

def blood_attack(targets, battle, enemy):        #enemy - ии, который использует скилл
    res = attack_func(targets, battle, enemy)
    for i in targets:
        battle.buff_list.get(i.nickname).get("power").append(BattleBuff(buff=-2, turns= 1 + 1))
    enemy.skill_cooldown.update({"Blood attack": 2 + 1})
    return res + ", " + str("-2 power")


AIDSEnemy_first_skill = Skill("Blood attack", "•<b>{0}</b>  использовал <b>Blood attack</b> на  <b>{1}</b>  {2}\n", 2, blood_attack)


def ass_taunt(targets, battle, enemy):
    team = 1
    battle.taunt_list.get(team).update({enemy.nickname: 2 + 1})
    enemy.skill_cooldown.update({"Ass taunt": 4 + 1})
    return "🔰"


AIDSEnemy_second_skill = Skill("Ass taunt", "•<b>{0}</b>  использовал <b>Ass attack</b> на  <b>{1}</b>  {2}\n", 6, ass_taunt)
