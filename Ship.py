
import wx
import math

import HUD
import Vector
import Scalar
import World

import ShipDesign
import ShipControls
import Autopilot
import Physics

MODULE_SIZE = 15

class Module:
	def __init__(self, parent, position, mass, color=None):
		self.parent = parent
		self.position = position
		self.mass = mass

		self.color = color
		
	def AbsolutePosition(self):
		relativePosition = Vector.Rotate(Vector.Scale(self.position, MODULE_SIZE), self.parent.rotation)
		return Vector.Add(relativePosition, self.parent.position)		

	def Draw(self, dc):
		x, y = self.AbsolutePosition()
		
		dc.SetPen(wx.Pen(wx.BLACK, 1))
		dc.SetBrush(wx.Brush(self.color))
		dc.DrawCircle(x, 720-y, MODULE_SIZE/2)

	def Simulate(self):
		pass
		
class Structure(Module):
	def __init__(self, parent, position):
		Module.__init__(self, parent, position, 2, wx.Colour(128, 128, 128))

class FlightComputer(Module):
	def __init__(self, parent, position):
		Module.__init__(self, parent, position, 10, wx.Colour(128, 128, 255))
		
		self.autopilot = None

	def Simulate(self):
		if self.autopilot == None:
			self.autopilot = Autopilot.Autopilot(ShipControls.ShipWrapper(self.parent))

		self.autopilot.Run()

class Engine(Module):
	def __init__(self, parent, position, thrustVector):
		Module.__init__(self, parent, position, 5, wx.Colour(64, 64, 64))
		
		self.thrustVector = thrustVector
		
		self.power = 0
		self.onTime = 0
		
	def CurrentThrust(self):
		return Vector.Scale(self.thrustVector, self.power)
		
	def Simulate(self):
		self.power = Scalar.Bound(0, self.power, 1)
	
		self.parent.ApplyLocalForce(self.CurrentThrust(), self.position)
		
	def Dizzy(self):
		return self.parent.CalculateDeltaSpinDueToLocalForce(self.thrustVector, self.position)
		
	def Acceleration(self):
		return Vector.Scale(self.thrustVector, 1.0 / self.parent.Mass())
		
	def Draw(self, dc):
		if self.power > 0.01:
			self.onTime += 1
		else:
			self.onTime -= 1

		self.onTime = Scalar.Bound(0, self.onTime, 20)

			
		if self.onTime > 0:
			visualPower = self.onTime / 20.0
			visualPower = (visualPower / 2.0) + 0.5
			visualPower = visualPower * -1
		
			jetVector = Vector.Scale(Vector.Normalize(self.thrustVector), visualPower)
			
			jetPoint = Vector.Add(self.position, jetVector)
			jetPosition = Vector.Rotate(Vector.Scale(jetPoint, MODULE_SIZE), self.parent.rotation)
			jetAbsolutePosition = Vector.Add(jetPosition, self.parent.position)
			x, y = jetAbsolutePosition
			
			dc.SetPen(wx.TRANSPARENT_PEN)
			dc.SetBrush(wx.Brush(wx.Colour( int(255.0 * abs(visualPower)), int(128.0 * abs(visualPower)), 0, self.onTime * 10 )))
			dc.DrawCircle(x, 720-y, 0.75 * MODULE_SIZE * abs(visualPower) * Vector.Magnitude(self.thrustVector))

		Module.Draw(self, dc)

class Explosion(Physics.PointBody):
	def __init__(self, position, velocity, size):
		Physics.PointBody.__init__(self, position)
		
		self.position = position
		self.velocity = velocity
		self.size = size
		
		self.initialLife = size
		self.life = size
	
	def Simulate(self):
		Physics.PointBody.Simulate(self)

		self.life -= 1
		
		if self.life < 5:
			self.destroyed = True
			
	def Mass(self):
		return 50000
		
	def Draw(self, dc):
		x, y = self.position
		alpha = int(200 * ((self.life+0.0) / self.initialLife))
		
		dc.SetPen(wx.Pen(wx.BLACK, 0))
		dc.SetBrush(wx.Brush(wx.Colour(255, 128, 0, alpha)))
		dc.DrawCircle(x, 720-y, self.life)		
		
	def SolidFor(self, object):
		return False
		

class Bullet(Physics.PointBody):
	def __init__(self, position, velocity, owner):
		Physics.PointBody.__init__(self, position)
		
		self.deflectorHold = True
		self.velocity = velocity
		self.owner = owner
		
	def Mass(self):
		return 1.0
		
	def Simulate(self):
		Physics.PointBody.Simulate(self)
		
		if Vector.Distance(self.position, self.owner.position) >= 200:
			self.deflectorHold = False
	
	def Draw(self, dc):
		x, y = self.position
		
		dc.SetPen(wx.Pen(wx.BLACK, 0))
		dc.SetBrush(wx.Brush(wx.BLACK))
		dc.DrawCircle(x, 720-y, 5)
		
	def SolidFor(self, object):
		if self.deflectorHold and object == self.owner:
			return False
		
		return True


class Railgun(Module):
	def __init__(self, parent, position):
		Module.__init__(self, parent, position, 5, wx.Colour(255, 0, 255))
		self.recharge = 0
		
	def Fire(self):
		if self.recharge > 0:
			return
			
		self.recharge = self.parent.world.RandomValue(15, 45)
		
		bulletStart = Vector.Add(self.position, [1, 0])
		offset = Vector.Scale(Vector.Rotate(bulletStart, self.parent.rotation), MODULE_SIZE)
		position = Vector.Add(self.parent.position, offset)
		
		self.parent.world.AddObject(Bullet(position, Vector.Rotate([MODULE_SIZE, 0], self.parent.rotation), self.parent))
	
	def Simulate(self):
		if self.recharge > 0:
			self.recharge -= 1
			
class Deflector(Module):
	def __init__(self, parent, position):
		self.range = 200
		self.availablePower = 1.0
		Module.__init__(self, parent, position, 15, wx.Colour(0, 255, 0))
	
	def Simulate(self):
		for object in self.parent.world.all[:]:
			if object == self.parent:
				continue
				
			if not object.SolidFor(self.parent):
				continue
			
			distance = Vector.Distance(object.position, self.AbsolutePosition())
			if distance > self.range or distance < 1:
				continue
			
			power = (self.range - distance + 0.0) / self.range
			power = power * self.availablePower
			power = power ** 2
			towardsObject = Vector.Normalize(Vector.Offset(object.position, self.parent.position))
			deflectorForce = Vector.Scale(towardsObject, power * 3)
			object.ApplyForce(deflectorForce)
			
			totalForce = Vector.Magnitude(deflectorForce)
			self.availablePower -= (totalForce * 0.01)
			
	def Draw(self, dc):
		Module.Draw(self, dc)
		
		x, y = self.AbsolutePosition()
		c = int(255 * self.availablePower)
		
		dc.SetPen(wx.Pen(wx.BLACK, 0))
		dc.SetBrush(wx.Brush(wx.Colour(255 - c, 128, c, 50)))
		dc.DrawCircle(x, 720-y, 50)		
			

class Ship(Physics.RigidBody):
	def __init__(self, shipType, position, world):
		Physics.RigidBody.__init__(self, position)
		
		self.world = world
		self.rotation = (math.pi/2) + (math.pi * shipType)
		
		self.flightComputer = None
		self.modules = []
		
		for moduleType, x, y in ShipDesign.AllModules(shipType):
			module = None
			
			if moduleType == "C":
				module = FlightComputer(self, [x, y])
				self.flightComputer = module
				
			elif moduleType == "S":
				module = Structure(self, [x, y])
			elif moduleType == "<":
				module = Engine(self, [x, y], [2, 0])
			elif moduleType == ">":
				module = Engine(self, [x, y], [-2, 0])
			elif moduleType == "]":
				module = Engine(self, [x, y], [-1, 0])
			elif moduleType == "[":
				module = Engine(self, [x, y], [1, 0])
			elif moduleType == "R":
				module = Railgun(self, [x, y])
			elif moduleType == "D":
				module = Deflector(self, [x, y])
			
			self.modules.append(module)
			
		self.engines = [m for m in self.modules if isinstance(m, Engine)]
		self.weapons = [r for r in self.modules if isinstance(r, Railgun)]
		
	def ScanForTargets(self):
		return [ t for t in self.world.Scan() if t != self ]

	def CenterOfMass(self):
		x = Vector.Sum([m.mass * m.position[0] for m in self.modules]) / len(self.modules)
		y = Vector.Sum([m.mass * m.position[1] for m in self.modules]) / len(self.modules)
		
		return [x, y]

	def Mass(self):
		return Vector.Sum([m.mass for m in self.modules])
		
	def MomentOfInertia(self):
		def MassRadiusSquared(module):
			radius = Vector.Magnitude(Vector.Offset(module.position, self.CenterOfMass()))
			return module.mass * radius * radius
			
		return Vector.Sum([MassRadiusSquared(m) for m in self.modules])

	def Draw(self, dc):
		for m in self.modules:
			m.Draw(dc)
		
	def Simulate(self):
		Physics.RigidBody.Simulate(self)
		
		HUD.frameOfReference = (self.position, self.rotation)
		
		for m in self.modules:
			m.Simulate()
			
		for item in self.world.all[:]:
			if item == self or not item.SolidFor(self):
				continue
			
			for module in self.modules[:]:
				if abs(Vector.Magnitude(Vector.Offset(item.position, module.AbsolutePosition()))) < (2.0 * Vector.Magnitude(item.velocity)):
					item.destroyed = True
					self.modules.remove(module)
					
					self.world.AddObject(Explosion(module.AbsolutePosition(), self.velocity, 50))
					
		if not (self.flightComputer in self.modules):
			self.world.AddObject(Explosion(module.AbsolutePosition(), self.velocity, 150))
			self.destroyed = True

					
					
