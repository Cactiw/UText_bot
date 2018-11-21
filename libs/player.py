import math
from work_materials.globals import dispatcher, cursor, conn, players_need_update, updating_cursor
from bin.equipment_service import *

class Player:

    stats = {}

    def __init__(self, id, username, nickname, sex, race, fraction, game_class):
        self.id = id
        self.username = username
        self.nickname = nickname

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

        self.first_skill_lvl = 1
        self.second_skill_lvl = 1
        self.third_skill_lvl = 0
        self.fourth_skill_lvl = 0
        self.fifth_skill_lvl = 0

        self.stats = {'endurance': 5, 'power': 5, 'armor': 5, 'charge': 5,
                    'speed': 5, }

        self.charge = self.stats['charge'] * 15
        self.hp = self.stats['endurance'] * 15
        self.take_damage_by_armor = 0

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

        self.eq_backpack = {}
        self.al_backpack = {}
        self.res_backpack = {}

    def add_item(self, list, item, count): # Добавление item в рюкзак list
        quanty = list.get(item.id)
        print(quanty)
        if quanty is None:
            quanty = int(count)
            list.update({item.id: quanty})
            print(list)
            request = "INSERT INTO inventory(user_id, type, id, quanty) VALUES('{0}', '{1}', '{2}', '{3}')".format(self.id, item.type,
                                                                                                 item.id, quanty)
            cursor.execute(request)
            conn.commit()
            #print("Item added to database")
            return
        quanty += int(count)
        list.update({item.id: quanty})
        print(list)
        request = "UPDATE inventory SET quanty = '{2}' WHERE user_id = '{0}' and id = '{1}'".format(self.id, item.id, quanty)
        cursor.execute(request)
        conn.commit()
        #print("Item quanty edited in database")
        return 0

    def remove_item(self, list, item, count):
        quanty = list.get(item.id)
        if quanty is None:
            return -1
        if quanty < count:
            return 1
        if quanty == count:
            list.pop(item.id)
            request = "DELETE FROM inventory WHERE user_id = '{0}' and id = '{1}'".format(self.id, item.id)
            cursor.execute(request)
            conn.commit()
            return 0
        quanty -= int(count)
        list.update({item.id: quanty})
        print(list)
        request = "UPDATE inventory SET type = '{1}', quanty = '{3}' WHERE user_id = '{0}'" \
                  " and id = '{2}'".format(self.id, item.type, item.id, quanty)
        cursor.execute(request)
        conn.commit()
        return 0


    def lvl_up_skill(self, skill_number):
        if(skill_number == '1'): self.first_skill_lvl += 1
        elif(skill_number == "2"): self.second_skill_lvl += 1
        elif(skill_number == "3"): self.third_skill_lvl += 1
        elif(skill_number == "4"): self.fourth_skill_lvl += 1
        elif(skill_number == "5"): self.fifth_skill_lvl += 1
        else: return None

    def lvl_up_point(self, stat):
        if(stat == "Выносливость"): self.stats["endurance"] += 1
        elif(stat == "Броня"): self.stats["armor"] += 1
        elif(stat == "Сила"): self.stats["power"] += 1
        elif(stat == "Скорость"): self.stats["speed"] += 1
        elif(stat == "Заряд"): self.stats["charge"] += 1
        else: return None

    @staticmethod
    def lvl_up(self):
        self.lvl += 1
        self.free_points += 5 #TODO balance
        self.free_skill_points += 1
        self.stats["endurance"] += 1
        self.stats["power"] += 1
        self.stats["armor"] += 1
        self.stats["charge"] += 1
        self.stats["speed"] += 1
        if self.game_class == "Warrior":
            self.stats["armor"] += 1
        elif self.game_class == "Mage" or self.game_class == "Cleric":
            self.stats["charge"] += 1
        elif self.game_class == "Archer":
            self.stats["speed"] += 1
        dispatcher.bot.send_message(chat_id = self.id, text = "LEVELUP!\nUse /lvl_up to choose a skill to upgrade")
        #TODO send message + choose_skill

    def lvl_check(self):
        if self.lvl < 50 and self.exp >= int(((self.lvl + 1) ** 3) * math.log(self.lvl + 1, math.e)):
            self.lvl_up(self)

    def equip(self, equipment): # Надевание предмета
        if self.on_character[equipment.place] is not None:
            on_equipment = get_equipment(self.on_character[equipment.place])
            self.unequip(on_equipment)
            pass
        return_key = self.remove_item(self.eq_backpack, equipment, 1)
        if return_key != 0:
            print(return_key)
            return return_key
        self.on_character[equipment.place] = equipment.id
        for i in self.stats:
            self.stats.update({i: self.stats.get(i) + equipment.stats.get(i)})
        players_need_update.put(self)
        #print("after equip", self.stats)


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
                  "head, body, shoulders, legs, feet, left_arm, right_arm, mount FROM players WHERE id = {0}".format(self.id)
        cursor.execute(request)
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
        self.first_skill_lvl = row[12]
        self.second_skill_lvl = row[13]
        self.third_skill_lvl = row[14]
        self.fourth_skill_lvl = row[15]
        self.fifth_skill_lvl = row[16]
        self.stats.update(endurance = row[17], power = row[18], armor = row[19], charge = row[20], speed = row[21])
        self.charge = row[22]
        self.hp = row[23]
        self.location = row[24]
        self.resources.update(gold = row[25], metal = row[26], wood = row[27])

        self.on_character.update(head = row[28] if row[28] != 'None' else None, body = row[29] if row[29] != 'None' else None,
                                 shoulders = row[30] if row[30] != 'None' else None, legs = row[31] if row[31] != 'None' else None,
                                 feet = row[32] if row[32] != 'None' else None, left_arm = row[33] if row[33] != 'None' else None,
                                 right_arm = row[34] if row[34] != 'None' else None, mount = row[35] if row[35] != 'None' else None)
        request = "SELECT type, id, quanty FROM inventory WHERE user_id = '{0}'".format(self.id)
        cursor.execute(request)
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
        cursor = conn.cursor()
        request = "UPDATE players SET id = '{0}', username = '{1}', nickname = '{2}', sex = '{3}', fraction = '{4}', " \
                  "race = '{5}', game_class = '{6}', exp = '{7}', lvl = '{8}', free_points = '{9}', free_skill_points = '{10}', fatigue = '{11}', " \
                  "first_skill_lvl = '{12}', second_skill_lvl = '{13}', third_skill_lvl = '{14}', fourth_skill_lvl = '{15}', " \
                  "fifth_skill_lvl = '{16}', endurance = '{17}', power = '{18}', armor = '{19}', charge = '{20}', speed = '{21}', " \
                  "mana = '{22}', hp = '{23}', location = '{24}', gold = '{25}', metal = '{26}', wood = '{27}', " \
                  "head = '{28}', body = '{29}', shoulders = '{30}', legs = '{31}', feet = '{32}', left_arm = '{33}', " \
                  "right_arm = '{34}', mount = '{35}' WHERE id = '{36}'".format(self.id, self.username, self.nickname, self.sex,
                                                           self.fraction, self.race, self.game_class, self.exp, self.lvl,
                                                           self.free_points, self.free_skill_points, self.fatigue,
                                                           self.first_skill_lvl,self.second_skill_lvl, self.third_skill_lvl,
                                                           self.fourth_skill_lvl, self.fifth_skill_lvl, self.stats['endurance'],
                                                           self.stats['power'], self.stats['armor'],
                                                           self.stats['charge'], self.stats['speed'],
                                                           self.charge, self.hp, self.location,
                                                           self.resources['gold'], self.resources['metal'],
                                                           self.resources['wood'], self.on_character['head'],
                                                           self.on_character['body'], self.on_character['shoulders'],
                                                           self.on_character['legs'], self.on_character['feet'],
                                                           self.on_character['left_arm'], self.on_character['right_arm'],
                                                           self.on_character['mount'], self.id)
        cursor.execute(request)             #   КРАЙНЕ НЕСТАБИЛЬНАЯ РАБОТА  TODO разобраться
        conn.commit()

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
                  " VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', " \
                  "'{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}'," \
                  "'{16}', '{17}','{18}','{19}', '{20}', '{21}', '{22}', '{23}', '{24}'," \
                  "'{25}', '{26}', '{27}', '{28}', '{29}', '{30}', '{31}', '{32}', '{33}', '{34}', '{35}')".format(self.id, self.username, self.nickname, self.sex,
                                                           self.fraction, self.race, self.game_class, self.exp, self.lvl,
                                                           self.free_points, self.free_skill_points, self.fatigue, self.first_skill_lvl,
                                                           self.second_skill_lvl, self.third_skill_lvl, self.fourth_skill_lvl, self.fifth_skill_lvl, self.stats['endurance'],
                                                           self.stats['power'], self.stats['armor'],
                                                           self.stats['charge'], self.stats['speed'],
                                                           self.charge, self.hp, self.location,
                                                           self.resources['gold'], self.resources['metal'],
                                                           self.resources['wood'], self.on_character['head'],
                                                           self.on_character['body'], self.on_character['shoulders'],
                                                           self.on_character['legs'], self.on_character['feet'],
                                                           self.on_character['left_arm'], self.on_character['right_arm'],
                                                           self.on_character['mount'])
        cursor.execute(request)
        conn.commit()
        #request = "CREATE TABLE inv_{0} (" \
        #          "type varchar(2)," \
        #          "id int(4)," \
        #          "quanty int(4)" \
        #          ");".format(self.id) #TODO сделать ключ к таблице с экипировкой
        #cursor.execute(request)
        #conn.commit()
