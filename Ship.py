
import wx
import Vector
import math
import Autopilot

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
		
		self.power = 0.2
		
	def CurrentThrust(self):
		return Vector.Scale(self.thrustVector, self.power)
		
	def Simulate(self):
		if self.power > 1:
			self.power = 1
		elif self.power < -1:
			self.power = -1
	
		# Velocity
		thrust = Vector.Rotate(self.CurrentThrust(), self.parent.rotation)
		deltaV = Vector.Scale(thrust, 1.0/self.parent.Mass())
		
		self.parent.velocity = Vector.Add(self.parent.velocity, deltaV)
		
		# Rotation
		self.parent.spin += self.DeltaSpinAtPower(self.power)
		
	def DeltaSpinAtPower(self, power):
		dx, dy = Vector.Offset(self.parent.CenterOfMass(), self.position)
		tx, ty = Vector.Scale(self.thrustVector, abs(power))
		
		torque = dx*ty - dy*tx
		torque = torque * -Vector.Sign(power)
		return torque / self.parent.MomentOfInertia()
		
	def Draw(self, dc):
		jetVector = Vector.Scale(self.thrustVector, -Vector.Sign(self.power))
		jetPoint = Vector.Add(self.position, jetVector)
		jetPosition = Vector.Rotate(Vector.Scale(jetPoint, 20), self.parent.rotation)
		jetAbsolutePosition = Vector.Add(jetPosition, self.parent.position)
		x, y = jetAbsolutePosition
		
		dc.SetBrush(wx.Brush(wx.Colour( int(255.0 * abs(self.power)), int(128.0 * abs(self.power)), 0 )))
		dc.DrawCircle(x, y, 15 * self.power)

		Module.Draw(self, dc)

class Ship:
	def __init__(self):
		nose = Structure(self, [0, 1])
		flightComputer = FlightComputer(self, [0, 0])
		
		leftPod = Structure(self, [2, 0])
		leftEngine = Engine(self, [1, 0], [0, 1])
		
		rightPod = Structure(self, [-2, 0])
		rightEngine = Engine(self, [-1, 0], [0, 1])
		
		self.position = [ 1280/2, 720/2 ]
		self.velocity = [ 0, 0 ]
		
		self.rotation = 0
		self.spin = 0.15
		
		self.modules = [ nose, flightComputer, leftPod, leftEngine, rightPod, rightEngine  ]
		self.engines = [ leftEngine, rightEngine ]

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
		dc.SetPen(wx.Pen(wx.BLACK, 2))
		
		for m in self.modules:
			m.Draw(dc)
		
		dc.DrawLine(0, 0, 50, 50)
		
	def Simulate(self):
		self.position = Vector.Add(self.position, self.velocity)
		self.rotation = (self.rotation + self.spin) % (2 * math.pi)
	
		for m in self.modules:
			m.Simulate()
