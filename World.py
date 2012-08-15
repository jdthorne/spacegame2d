

class World:
	def __init__(self):
		self.all = []

	def Scan(self):
		return self.all[:]
		
	def AddObject(self, object):
		self.all.append(object)
		
	def RemoveObject(self, object):
		self.all.remove(object)
		
class WorldItem:
	destroyed = False
	
	def Draw(self):
		pass
		
	def Simulate(self):
		pass
		
	def SolidFor(self, object):
		return True