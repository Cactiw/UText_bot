from libs.locations.location import *

class Portal(Location):

	def __init__(self, id, name, fraction):
		super(Portal, self).__init__(id, name)
		self.fraction = fraction #фракция, которая контроллирует точку
		self.avaliable = 0

portal = Portal(1, "Портал", None)