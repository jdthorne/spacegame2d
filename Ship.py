
import wx
import Vector
import math
import Autopilot

class Module:
	def __init__(self, parent, position, color, mass):
		self.parent = parent
		self.position = position
		self.color = color
		self.mass = mass
		
	def Color(self):
		return self.color

	def Simulate(self):
		pass
		
class StructuralSupport(Module):
	def __init__(self, parent, position):
		Module.__init__(self, parent, position, wx.GREEN, 2)

class FlightComputer(Module):
	def __init__(self, parent, position):
		Module.__init__(self, parent, position, wx.BLUE, 10)
		
		self.autopilot = Autopilot.Autopilot()

	def Simulate(self):
		self.autopilot(self.parent)

class Engine(Module):
	def __init__(self, parent, position, thrustVector):
		Module.__init__(self, parent, position, wx.RED, 5)
		
		self.thrustVector = thrustVector
		
		self.power = 0.2
		
	def CurrentThrust(self):
		return Vector.Scale(self.thrustVector, self.power)
		
	def Simulate(self):
		if self.power > 1:
			self.power = 1
	
		# Velocity
		thrust = Vector.Rotate(self.CurrentThrust(), self.parent.rotation)
		deltaV = Vector.Scale(thrust, 1.0/self.parent.Mass())
		
		self.parent.velocity = Vector.Add(self.parent.velocity, deltaV)
		
		# Rotation
		self.parent.spin += self.DeltaSpinAtPower(self.power)
		
	def DeltaSpinAtPower(self, power):
		dx, dy = Vector.Offset(self.parent.CenterOfMass(), self.position)
		tx, ty = Vector.Scale(self.thrustVector, power)

		torque = dx*ty - dy*tx
		return torque / self.parent.MomentOfInertia()
		
	def Color(self):
		if abs(self.power) > 0.01:
			return wx.RED
		
		return wx.BLACK

class Ship:
	def __init__(self):
		nose = StructuralSupport(self, [0, 1])
		flightComputer = FlightComputer(self, [0, 0])
		leftEngine = Engine(self, [1, 0], [0, 1])
		rightEngine = Engine(self, [-1, 0], [0, 1])
		
		self.position = [ 1280/2, 720/2 ]
		self.velocity = [ 0, 0 ]
		
		self.rotation = 0
		self.spin = 0
		
		self.modules = [ nose, flightComputer, leftEngine, rightEngine  ]
		self.engines = [ leftEngine, rightEngine ]

	def CenterOfMass(self):
		x = Vector.Sum([m.mass * m.position[0] for m in self.modules])
		y = Vector.Sum([m.mass * m.position[1] for m in self.modules])
		
		return [x, y]

	def Mass(self):
		return Vector.Sum([m.mass for m in self.modules])
		
	def MomentOfInertia(self):
		def MassRadiusSquared(module):
			radius = Vector.Magnitude(Vector.Offset(module.position, self.CenterOfMass()))
			return module.mass * radius * radius
			
		return Vector.Sum([MassRadiusSquared(m) for m in self.modules])

	def Draw(self, dc):
		dc.SetPen(wx.Pen(wx.BLACK, 2))
		
		for m in self.modules:
			relativePosition = Vector.Rotate(Vector.Scale(m.position, 20), self.rotation)
			absolutePosition = Vector.Add(relativePosition, self.position)
			
			x, y = absolutePosition
			
			dc.SetBrush(wx.Brush(m.Color()))
			dc.DrawCircle( x, y, 10)
		
		dc.DrawLine(0, 0, 50, 50)
		
	def Simulate(self):
		self.position = Vector.Add(self.position, self.velocity)
		self.rotation = (self.rotation + self.spin) % (2 * math.pi)
	
		for m in self.modules:
			m.Simulate()
