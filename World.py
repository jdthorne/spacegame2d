import random

class World:
	def __init__(self):
		random.seed(500)
		self.all = []

	def Scan(self):
		return self.all[:]
		
	def AddObject(self, object):
		self.all.append(object)
		
	def RemoveObject(self, object):
		self.all.remove(object)
		
	def RandomValue(self, a, b):
		return random.randint(a, b)
		
class WorldItem:
	destroyed = False
	
	def Draw(self):
		pass
		
	def Simulate(self):
		pass
		
	def SolidFor(self, object):
		return True
		
	def DeflectedBy(self, object):
		return True