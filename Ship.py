
import wx
import math

import Vector
import Scalar

import Autopilot
import Physics

class Module:
	def __init__(self, parent, position, mass, color=None):
		self.parent = parent
		self.position = position
		self.mass = mass

		self.color = color

	def Draw(self, dc):
		relativePosition = Vector.Rotate(Vector.Scale(self.position, 20), self.parent.rotation)
		absolutePosition = Vector.Add(relativePosition, self.parent.position)
		x, y = absolutePosition
		
		dc.SetPen(wx.Pen(wx.BLACK, 2))
		dc.SetBrush(wx.Brush(self.color))
		dc.DrawCircle(x, y, 10)

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
		self.autopilot(self.parent)

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
		
			jetVector = Vector.Scale(self.thrustVector, visualPower)
			
			jetPoint = Vector.Add(self.position, jetVector)
			jetPosition = Vector.Rotate(Vector.Scale(jetPoint, 20), self.parent.rotation)
			jetAbsolutePosition = Vector.Add(jetPosition, self.parent.position)
			x, y = jetAbsolutePosition
			
			dc.SetPen(wx.TRANSPARENT_PEN)
			dc.SetBrush(wx.Brush(wx.Colour( int(255.0 * abs(visualPower)), int(128.0 * abs(visualPower)), 0 )))
			dc.DrawCircle(x, y, 15 * abs(visualPower))

		Module.Draw(self, dc)

class Ship(Physics.PhysicsBody):
	def __init__(self):
		Physics.PhysicsBody.__init__(self)
	
		nose = Structure(self, [0, 1])
		flightComputer = FlightComputer(self, [0, 0])
		core = [ nose, flightComputer ]
		
		leftPod = Structure(self, [2, 0])
		rightPod = Structure(self, [-2, 0])
		pods = [ leftPod, rightPod ]
		
		leftBrake = Engine(self, [1, 0], [0, -1])		
		rightBrake = Engine(self, [-1, 0], [0, -1])
		brakeEngines = [ leftBrake, rightBrake ]
		
		leftThrust = Engine(self, [2, -1], [0, 1])
		rightThrust = Engine(self, [-2, -1], [0, 1])
		thrustEngines = [ leftThrust, rightThrust ]
		
		self.modules = core + pods + brakeEngines + thrustEngines
		
		self.engines = brakeEngines + thrustEngines
		self.thrustEngines = thrustEngines

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
		
		dc.DrawLine(0, 0, 50, 50)
		
	def Simulate(self):
		self.position = Vector.Add(self.position, self.velocity)
		self.rotation = (self.rotation + self.spin) % (2 * math.pi)
	
		for m in self.modules:
			m.Simulate()
