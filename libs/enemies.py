from work_materials.globals import *
from random import randint
from libs.buff import *


class Enemy:
	def __init__(self, id, name, lvl):
		self.id = id
		self.name = name
		self.lvl = lvl


class AIDSEnemy(Enemy):
	def __init__(self, lvl):
		super(AIDSEnemy, self).__init__(1, "AIDS", lvl)

		self.stats = {'endurance': 3, 'power': 3, 'armor': 3, 'charge': 3, 'speed': 3}
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
			else :
				self.stats['speed'] += 1


		self.skill_names = ['blood atack', 'ass atack']

		self.charge = self.stats['charge'] * 13
		self.hp = self.stats['endurance'] * 13
		#self.damage_taken_by_armor = 0

	def blood_atack(self, target):
		target.hp -= self.stats.get('power') * 4
		if target.hp <= 0:
			target.dead = 1

	def ass_atack(self, target):
		name = "Ass Pain"
		buff = Buff(name, {'power': -2, 'armor': -2}, 2)
		target.buffs.update({name: buff})
