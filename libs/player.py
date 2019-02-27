import math
import work_materials.globals as globals
from work_materials.globals import dispatcher, players_need_update, skills
from bin.equipment_service import *


class Player:

    stats = {}

    def __init__(self, id, username, nickname, sex, race, fraction, game_class):
        self.id = id
        self.username = username
        self.nickname = nickname

        self.dead = 0

        self.status = "In Location"

        self.sex = sex
        self.race = race
        self.fraction = fraction
        self.game_class = game_class

        self.exp = 0
        self.lvl = 1
        self.free_points = 5
        self.free_skill_points = 2
        self.fatigue = 0

        self.battle_id = -1

        self.skill_lvl = {}
        self.skill_cooldown = {}

        self.stats = {'endurance': 5, 'power': 5, 'armor': 5, 'charge': 5,
                    'speed': 5} #speed == Ловкость (evade)

        self.charge = int(self.stats['charge'] * (self.lvl ** (3/2) + 20))
        self.hp = int(self.stats['endurance'] * 3 * (self.lvl ** (3/2) + 20))

        self.location = 0

        if self.fraction == 'Федералы':
            self.location = 14
        elif self.fraction == 'Трибунал':
            self.location = 15
        elif self.fraction == 'Стая':
            self.location = 16

        self.resources = {'gold' : 0, 'metal' : 0, 'wood' : 0}

        self.on_character = {'head': None, 'body': None, 'shoulders': None, 'legs': None, 'feet': None,
                        'left_arm': None, 'right_arm': None, 'mount': None, }

        self.buffs = {}
        self.debuffs = {}

        self.eq_backpack = {}
        self.al_backpack = {}
        self.res_backpack = {}

    def update_skills(self):
        class_skills = skills.get(self.game_class)
        for i in list(class_skills):
            if i == 'Атака' or i == 'Пропуск хода':
                continue
            self.skill_cooldown.update({i: 0})
            self.skill_lvl.update({i: 1})

    def update_cooldown(self):
        class_skills = skills.get(self.game_class)
        for i in list(class_skills.values()):
            if i.name == 'Атака' or i.name == 'Пропуск хода':
                continue
            self.skill_cooldown.update({i.name: 0})

    def update_stats(self):
        self.charge = int(self.stats['charge'] * (self.lvl ** (3 / 2) + 20))
        self.hp = int(self.stats['endurance'] * 3 * (self.lvl ** (3 / 2) + 20))

    def __eq__(self, other):    # Два игрока равны ТИТТК равны их id
        return self.id == other.id

    def add_item(self, list, item, count): # Добавление item в рюкзак list
        quanty = list.get(item.id)
        if quanty is None:
            quanty = int(count)
            list.update({item.id: quanty})
            request = "INSERT INTO inventory(user_id, type, id, quanty) VALUES(%s, %s, %s, %s)"
            cursor.execute(request, (self.id, item.type, item.id, quanty))
            conn.commit()
            return
        quanty += int(count)
        list.update({item.id: quanty})
        request = "UPDATE inventory SET quanty = %s WHERE user_id = %s and id = %s"
        cursor.execute(request, (self.id, item.id, quanty))
        conn.commit()
        return 0

    def remove_item(self, list, item, count):
        quanty = list.get(item.id)
        if quanty is None:
            return -1
        if quanty < count:
            return 1
        if quanty == count:
            list.pop(item.id)
            request = "DELETE FROM inventory WHERE user_id = %s and id = %s"
            cursor.execute(request, (self.id, item.id))
            conn.commit()
            return 0
        quanty -= int(count)
        list.update({item.id: quanty})
        request = "UPDATE inventory SET type = %s, quanty = %s WHERE user_id = %s" \
                  " and id = %s"
        cursor.execute(request, (self.id, item.type, item.id, quanty))
        conn.commit()
        return 0

    def skill_avaliable(self, skill_name): #-1 - нет такого скилла, -2 - не разблокирован, -3 - КД
        if skill_name == 'Атака' or skill_name == 'Пропуск хода':
            return 1
        avaliable_skills = skills.get(self.game_class)
        flag = 0
        for i in list(avaliable_skills.values()):
            if i.name == skill_name:
                flag = 1
                break
        if flag == 0:
            return -1
        for i in range(len(list(avaliable_skills.values()))):
            if list(avaliable_skills.values())[i].name == skill_name:
                if self.skill_lvl.get(skill_name) <= 0:
                    return -2
                else:
                    if self.skill_cooldown.get(skill_name) > 0:
                        return -3
                    else:
                        return 1

    def lvl_up_skill(self, skill_number):
        if int(skill_number) not in range(6):
            return None
        skill_names = list(skills.get(self.game_class))
        self.skill_lvl.update({skill_names[int(skill_number)]: int(self.skill_lvl.get(skill_names[int(skill_number)])) + 1})

    def lvl_up_point(self, stat):
        if stat == "Выносливость":
            self.stats["endurance"] += 1
        elif stat == "Броня":
            self.stats["armor"] += 1
        elif stat == "Сила":
            self.stats["power"] += 1
        elif stat == "Скорость":
            self.stats["speed"] += 1
        elif stat == "Заряд":
            self.stats["charge"] += 1
        else:
            return None

    def lvl_up(self):
        self.lvl += 1
        self.free_points += 3
        self.free_skill_points += 1
        dispatcher.bot.send_message(chat_id = self.id, text = "<b>LEVELUP!</b>\nUse /lvl_up to choose a skill to upgrade",
                                    parse_mode="HTML")

    def get_next_lvl_exp(self):
        return int(((self.lvl + 1) ** 3) * math.log(self.lvl + 1, math.e))

    def lvl_check(self):
        if self.lvl < 50 and self.exp >= int(((self.lvl + 1) ** 3) * math.log(self.lvl + 1, math.e)):
            self.lvl_up()

    def equip(self, equipment): # Надевание предмета
        if self.on_character[equipment.place] is not None:
            on_equipment = get_equipment(self.on_character[equipment.place])
            self.unequip(on_equipment)
            pass
        return_key = self.remove_item(self.eq_backpack, equipment, 1)
        if return_key != 0:
            return return_key
        self.on_character[equipment.place] = equipment.id
        for i in self.stats:
            self.stats.update({i: self.stats.get(i) + equipment.stats.get(i)})
        players_need_update.put(self)

    def unequip(self, equipment): # Снятие предмета
        self.add_item(self.eq_backpack, equipment, 1)
        self.on_character[equipment.place] = None
        for i in self.stats:
            self.stats.update({i: self.stats.get(i) - equipment.stats.get(i)})

    def change_location(self, location):
        self.location = location
        
    def update_from_database(self):
        request = "SELECT id, username, nickname, sex, fraction, race, game_class," \
                  " exp, lvl, free_points, free_skill_points, fatigue, first_skill_lvl, second_skill_lvl, " \
                  "third_skill_lvl, fourth_skill_lvl, fifth_skill_lvl, endurance, power, armor, charge, speed, mana, hp," \
                  " location, gold, metal, wood, " \
                  "head, body, shoulders, legs, feet, left_arm, right_arm, mount FROM players WHERE id = %s"
        cursor.execute(request, (self.id,))
        row = cursor.fetchone()
        if row is None:
            return None
        self.id = row[0]
        self.username = row[1]
        self.nickname = row[2]
        self.sex = row[3]
        self.fraction = row[4]
        self.race = row[5]
        self.game_class = row[6]
        self.exp = row[7]
        self.lvl = row[8]
        self.free_points = row[9]
        self.free_skill_points = row[10]
        self.fatigue = row[11]
        skill_names = list(skills.get(self.game_class))
        for i in range(len(skill_names)):
            if i in [0, len(skill_names) - 1]:
                continue
            self.skill_lvl.update({skill_names[i]: row[12 + i - 1]})
        self.stats.update(endurance = row[17], power = row[18], armor = row[19], charge = row[20], speed = row[21])
        self.charge = row[22]
        self.hp = row[23]
        self.location = row[24]
        self.resources.update(gold = row[25], metal = row[26], wood = row[27])

        self.on_character.update(head = row[28] if row[28] != 'None' else None, body = row[29] if row[29] != 'None' else None,
                                 shoulders = row[30] if row[30] != 'None' else None, legs = row[31] if row[31] != 'None' else None,
                                 feet = row[32] if row[32] != 'None' else None, left_arm = row[33] if row[33] != 'None' else None,
                                 right_arm = row[34] if row[34] != 'None' else None, mount = row[35] if row[35] != 'None' else None)
        request = "SELECT type, id, quanty FROM inventory WHERE user_id = %s"
        cursor.execute(request, (self.id,))
        row = cursor.fetchone()
        while row:
            type = row[0]
            id = row[1]
            quanty = row[2]
            if type == "a":
                self.al_backpack.update({id: quanty})
            elif type == "r":
                self.res_backpack.update({id: quanty})
            else:
                self.eq_backpack.update({id: quanty})
            row = cursor.fetchone()
        return self

    def update_to_database(self):
        request = "UPDATE players SET id = %s, username = %s, nickname = %s, sex = %s, fraction = %s, " \
                  "race = %s, game_class = %s, exp = %s, lvl = %s, free_points = %s, free_skill_points = %s, fatigue = %s, " \
                  "first_skill_lvl = %s, second_skill_lvl = %s, third_skill_lvl = %s, fourth_skill_lvl = %s, " \
                  "fifth_skill_lvl = %s, endurance = %s, power = %s, armor = %s, charge = %s, speed = %s, " \
                  "mana = %s, hp = %s, location = %s, gold = %s, metal = %s, wood = %s, " \
                  "head = %s, body = %s, shoulders = %s, legs = %s, feet = %s, left_arm = %s, " \
                  "right_arm = %s, mount = %s WHERE id = %s"
        globals.cursor.execute(request, (self.id, self.username, self.nickname, self.sex,
                                         self.fraction, self.race, self.game_class, self.exp, self.lvl,
                                         self.free_points, self.free_skill_points, self.fatigue,
                                         list(self.skill_lvl.values())[0], list(self.skill_lvl.values())[1], list(self.skill_lvl.values())[2],
                                         list(self.skill_lvl.values())[3], list(self.skill_lvl.values())[4], self.stats['endurance'],
                                         self.stats['power'], self.stats['armor'], self.stats['charge'], self.stats['speed'],
                                         self.charge, self.hp, self.location, self.resources['gold'], self.resources['metal'],
                                         self.resources['wood'], self.on_character['head'],
                                         self.on_character['body'], self.on_character['shoulders'],
                                         self.on_character['legs'], self.on_character['feet'],
                                         self.on_character['left_arm'], self.on_character['right_arm'],
                                         self.on_character['mount'], self.id))
        globals.conn.commit()

    def add_to_database(self):
        if self.sex == "Мужской":
            self.sex = 0
        else:
            self.sex = 1
        request = "INSERT INTO players(id, username, nickname, sex, fraction, race, game_class," \
                  " exp, lvl, free_points, free_skill_points, fatigue, first_skill_lvl, second_skill_lvl, " \
                  "third_skill_lvl, fourth_skill_lvl, fifth_skill_lvl, endurance, power, armor, charge, speed, mana, hp," \
                  " location, gold, metal, wood, " \
                  "head, body, shoulders, legs, feet, left_arm, right_arm, mount)" \
                  " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                  "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(request, (self.id, self.username, self.nickname, self.sex,
                                 self.fraction, self.race, self.game_class, self.exp, self.lvl,
                                 self.free_points, self.free_skill_points, self.fatigue, list(self.skill_lvl.values())[0],
                                 list(self.skill_lvl.values())[1], list(self.skill_lvl.values())[2],
                                 list(self.skill_lvl.values())[3], list(self.skill_lvl.values())[4], self.stats['endurance'],
                                 self.stats['power'], self.stats['armor'], self.stats['charge'], self.stats['speed'],
                                 self.charge, self.hp, self.location, self.resources['gold'], self.resources['metal'],
                                 self.resources['wood'], self.on_character['head'], self.on_character['body'],
                                 self.on_character['shoulders'], self.on_character['legs'], self.on_character['feet'],
                                 self.on_character['left_arm'], self.on_character['right_arm'], self.on_character['mount']))
        conn.commit()
