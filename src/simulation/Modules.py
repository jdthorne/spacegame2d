from Vector import *
from Scalar import *
import ShipControls
import Misc
import Ship
import Timing

class Module:
   isDeflector = False

   def __init__(self, parent, position, mass):
      self.parent = parent
      self.position = position
      self.mass = mass

   def __eq__(self, rhs):
      return self is rhs

   def absolutePosition(self):
      relativePosition = vectorRotate(self.position, self.parent.rotation)
      return vectorAdd(relativePosition, self.parent.position)      

   def simulate(self):
      pass
      
class Structure(Module):
   def __init__(self, parent, position):
      Module.__init__(self, parent, position, 2)

class FlightComputer(Module):
   def __init__(self, parent, position, autopilot):
      Module.__init__(self, parent, position, 10)
 
      self.autopilot = None     
      self.createAutopilot = autopilot

   def installAutopilot(self, autopilot):
      self.autopilot = None     
      self.createAutopilot = autopilot      

   def simulate(self):
      if self.autopilot == None:
         self.shipWrapper = ShipControls.ShipWrapper(self.parent)
         self.autopilot = self.createAutopilot(self.shipWrapper)

      self.runAutopilot()

   @Timing.timedFunction
   def runAutopilot(self):
      if self.parent.damaged:
         self.shipWrapper.updateAll()

      self.autopilot.run()
      self.parent.status = self.autopilot.status()

class Engine(Module):
   def __init__(self, parent, position, thrustVector):
      Module.__init__(self, parent, position, 3)
      
      self.thrustVector = thrustVector
      
      self.power = 0
      self.onTime = 0
      
   def currentThrust(self):
      return vectorScale(self.thrustVector, self.power)
      
   def simulate(self):
      self.power = scalarBound(0, self.power, 1)
   
      self.parent.applyLocalForce(self.currentThrust(), self.position)
      
   def dizzy(self):
      return self.parent.calculateDeltaSpinDueToLocalForce(self.thrustVector, self.position)
      
   def acceleration(self):
      return vectorScale(self.thrustVector, 1.0 / self.parent.mass())


class PlasmaCannon(Module):
   def __init__(self, parent, position):
      Module.__init__(self, parent, position, 5)
      self.recharge = 0
      
   def fire(self):
      if self.recharge > 0:
         return
         
      self.recharge = self.parent.world.randomValue(15, 45)
      
      bulletStart = vectorAdd(self.position, [1, 0])
      offset = vectorRotate(bulletStart, self.parent.rotation)
      position = vectorAdd(self.parent.position, offset)
      
      self.parent.world.addObject(Misc.Bullet(position, vectorRotate([Misc.BULLET_SPEED, 0], self.parent.rotation), self.parent))
   
   def simulate(self):
      if self.recharge > 0:
         self.recharge -= 1

   def ready(self):
      return (self.recharge == 0)
         
class Deflector(Module):
   def __init__(self, parent, position):
      Module.__init__(self, parent, position, 15)

      self.isDeflector = True
   
   def simulate(self):
      pass
