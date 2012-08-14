
import wx
import math

import Vector
import Scalar

import ShipDesign
import ShipControls
import Autopilot
import Physics

MODULE_SIZE = 20

class Module:
	def __init__(self, parent, position, mass, color=None):
		self.parent = parent
		self.position = position
		self.mass = mass

		self.color = color

	def Draw(self, dc):
		relativePosition = Vector.Rotate(Vector.Scale(self.position, MODULE_SIZE), self.parent.rotation)
		absolutePosition = Vector.Add(relativePosition, self.parent.position)
		x, y = absolutePosition
		
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
		
		self.autopilot = Autopilot.Autopilot()

	def Simulate(self):
		self.autopilot(ShipControls.ShipWrapper(self.parent))

class Engine(Module):
	def __init__(self, parent, position, thrustVector):
		Module.__init__(self, parent, position, 5, wx.Colour(64, 64, 64))
		
		self.thrustVector = thrustVector
		
		self.power = 0
		
	def CurrentThrust(self):
		return Vector.Scale(self.thrustVector, self.power)
		
	def Simulate(self):
		self.power = Scalar.Bound(0, self.power, 1)
	
		self.parent.ApplyForce(self.CurrentThrust(), self.position)
		
	def DeltaSpinAtPower(self, power):
		thrustAtPower = Vector.Scale(self.thrustVector, power)
		return self.parent.CalculateDeltaSpinDueToForce(thrustAtPower, self.position)
		
	def Draw(self, dc):
		if self.power > 0.01:
			visualPower = Scalar.Bound(0, self.power, 1)
			visualPower = (visualPower / 2) + 0.5
			visualPower = visualPower * -1
		
			jetVector = Vector.Scale(Vector.Normalize(self.thrustVector), visualPower)
			
			jetPoint = Vector.Add(self.position, jetVector)
			jetPosition = Vector.Rotate(Vector.Scale(jetPoint, MODULE_SIZE), self.parent.rotation)
			jetAbsolutePosition = Vector.Add(jetPosition, self.parent.position)
			x, y = jetAbsolutePosition
			
			dc.SetPen(wx.TRANSPARENT_PEN)
			dc.SetBrush(wx.Brush(wx.Colour( int(255.0 * abs(visualPower)), int(128.0 * abs(visualPower)), 0 )))
			dc.DrawCircle(x, 720-y, 0.75 * MODULE_SIZE * abs(visualPower) * Vector.Magnitude(self.thrustVector))

		Module.Draw(self, dc)

class Ship(Physics.PhysicsBody):
	def __init__(self, position, scanner=None, powered=False):
		Physics.PhysicsBody.__init__(self, position)
		
		self.scanner = scanner
		self.powered = powered
		
		self.modules = []
		
		for moduleType, x, y in ShipDesign.AllModules():
			module = None
			
			if moduleType == "C":
				module = FlightComputer(self, [x, y])
			elif moduleType == "S":
				module = Structure(self, [x, y])
			elif moduleType == "<":
				module = Engine(self, [x, y], [-2, 0])
			elif moduleType == "[":
				module = Engine(self, [x, y], [-1, 0])
			elif moduleType == "]":
				module = Engine(self, [x, y], [1, 0])
			
			self.modules.append(module)
			
		self.engines = [m for m in self.modules if isinstance(m, Engine)]
		
	def ScanForTargets(self):
		return [ t for t in self.scanner() if t != self ]

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
		self.position = Vector.Add(self.position, self.velocity)
		self.rotation = (self.rotation + self.spin) % (2 * math.pi)
	
		for m in self.modules:
			if self.powered:
				m.Simulate()
