
import math

import HUD
import Vector
import Scalar
import World

import Timing
import ShipDesign
import ShipControls
import Autopilot
import Physics

MODULE_SIZE = 40

class Module:
   def __init__(self, parent, position, mass):
      self.parent = parent
      self.position = position
      self.mass = mass
      
   def absolutePosition(self):
      relativePosition = Vector.rotate(self.position, self.parent.rotation)
      return Vector.add(relativePosition, self.parent.position)      

   def simulate(self):
      pass
      
class Structure(Module):
   def __init__(self, parent, position):
      Module.__init__(self, parent, position, 2)

class FlightComputer(Module):
   def __init__(self, parent, position):
      Module.__init__(self, parent, position, 10)
      
      self.autopilot = None

   @Timing.timedFunction("Simulate/Ship/Autopilot")
   def simulate(self):
      if self.autopilot == None:
         self.autopilot = Autopilot.Autopilot(ShipControls.ShipWrapper(self.parent))

      self.autopilot.run()

class Engine(Module):
   def __init__(self, parent, position, thrustVector):
      Module.__init__(self, parent, position, 3)
      
      self.thrustVector = thrustVector
      
      self.power = 0
      self.onTime = 0
      
   def currentThrust(self):
      return Vector.scale(self.thrustVector, self.power)
      
   @Timing.timedFunction("Simulate/Ship/Engine")
   def simulate(self):
      self.power = Scalar.bound(0, self.power, 1)
   
      self.parent.applyLocalForce(self.currentThrust(), self.position)
      
   def dizzy(self):
      return self.parent.calculateDeltaSpinDueToLocalForce(self.thrustVector, self.position)
      
   def acceleration(self):
      return Vector.scale(self.thrustVector, 1.0 / self.parent.mass())

class Explosion(Physics.PointBody):
   def __init__(self, position, velocity, size):
      Physics.PointBody.__init__(self, position)
      
      self.exciting = True
      self.position = position
      self.velocity = velocity
      self.size = size
      
      self.initialLife = size
      self.life = size
   
   def simulate(self):
      Physics.PointBody.simulate(self)

      self.life -= 1
      
      if self.life < 5:
         self.destroyed = True
         
   def mass(self):
      return 5
      
   def solidFor(self, object):
      return False
      

class Bullet(Physics.PointBody):
   def __init__(self, position, velocity, owner):
      Physics.PointBody.__init__(self, position)
      
      self.deflectorHold = True
      self.velocity = velocity
      self.owner = owner
      
      self.initialLife = 50
      self.life = self.initialLife
      
   def mass(self):
      return 1.0
      
   def simulate(self):
      self.life -= 1
      Physics.PointBody.simulate(self)
      
      if Vector.distance(self.position, self.owner.position) >= 200:
         self.deflectorHold = False
         
      if self.life < 0:
         self.destroyed = True
      
   def solidFor(self, object):
      if object == self.owner:
         return False
      
      return True


class PlasmaCannon(Module):
   def __init__(self, parent, position):
      Module.__init__(self, parent, position, 5)
      self.recharge = 0
      
   def fire(self):
      if self.recharge > 0:
         return
         
      self.recharge = self.parent.world.randomValue(15, 45)
      
      bulletStart = Vector.add(self.position, [1, 0])
      offset = Vector.rotate(bulletStart, self.parent.rotation)
      position = Vector.add(self.parent.position, offset)
      
      self.parent.world.addObject(Bullet(position, Vector.rotate([MODULE_SIZE, 0], self.parent.rotation), self.parent))
   
   def simulate(self):
      if self.recharge > 0:
         self.recharge -= 1
         
class Deflector(Module):
   def __init__(self, parent, position):
      self.range = 700
      self.availablePower = 1.0
      Module.__init__(self, parent, position, 15)
   
   @Timing.timedFunction("Simulate/Ship/Deflector")
   def simulate(self):
      for object in self.parent.world.all[:]:
         if object == self.parent:
            continue
            
         if not object.solidFor(self.parent):
            continue
         
         distance = Vector.distance(object.position, self.absolutePosition())
         if distance > self.range or distance < 1:
            continue
            
         #vectorTowardSelf = Vector.offset(self.parent.position, object.position)

         #relativeVelocity = Vector.offset(self.parent.velocity, object.velocity)
         #speedTowardSelf = Vector.scalarProjection(relativeVelocity, vectorTowardSelf)

         #if speedTowardSelf > 0:
         #   continue
         
         power = (self.range - distance + 0.0) / self.range
         power = power * self.availablePower
         power = power ** 2
         #towardsObject = Vector.normalize(Vector.offset(object.position, self.parent.position))
         #deflectorForce = Vector.scale(towardsObject, power * 6)
         #object.applyForce(deflectorForce)
         
         mix = 0.5 * power
         object.velocity = Vector.add(Vector.scale(object.velocity, 1.0 - mix), Vector.scale(self.parent.velocity, mix))
         
         delta = Vector.magnitude(Vector.offset(object.velocity, self.parent.velocity))

         self.availablePower -= (delta * power * 0.002)
         

class Ship(Physics.RigidBody):
   def __init__(self, shipType, position, world):
      Physics.RigidBody.__init__(self, position)
      
      self.combatTeam = shipType
      self.exciting = True
      self.world = world
      self.rotation = (math.pi/2) + (math.pi * shipType)
      
      self.flightComputer = None
      self.modules = []
      
      for moduleType, x, y in ShipDesign.allModules(shipType):
         x *= MODULE_SIZE
         y *= MODULE_SIZE
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
         elif moduleType == "P":
            module = PlasmaCannon(self, [x, y])
         elif moduleType == "D":
            module = Deflector(self, [x, y])
         
         self.modules.append(module)
         
      self.engines = [m for m in self.modules if isinstance(m, Engine)]
      self.weapons = [r for r in self.modules if isinstance(r, PlasmaCannon)]
      
      self.recalculateModules()
      
   def scanForTargets(self):
      return [ t for t in self.world.scan() if t != self ]

   def centerOfMass(self):
      x = Vector.sum([m.mass * m.position[0] for m in self.modules]) / self.mass()
      y = Vector.sum([m.mass * m.position[1] for m in self.modules]) / self.mass()
      
      return [x, y]

   def mass(self):
      return self.calculatedMass
      
   def momentOfInertia(self):
      return self.calculatedMomentOfInertia
      
   def recalculateModules(self):
      # Recalculate mass
      self.calculatedMass = Vector.sum([m.mass for m in self.modules])
      
      # Move to center of mass
      move = self.centerOfMass()      
      for m in self.modules:
         m.position = Vector.offset(m.position, move)
         
      self.position = Vector.add(self.position, move)
      
      # Recalculate moment of inertia
      def massRadiusSquared(module):
         radius = Vector.magnitude(module.position)
         return module.mass * radius * radius
         
      result = Vector.sum([massRadiusSquared(m) for m in self.modules])
      if result < 1.0:
         return 1.0
         
      self.calculatedMomentOfInertia = result

   @Timing.timedFunction("Simulate/Ship")
   def simulate(self):
      Physics.RigidBody.simulate(self)
      HUD.frameOfReference = (self.position, self.rotation)
      
      self.simulateAllModules()
      self.simulateCollisions()
      
   @Timing.timedFunction("Simulate/Ship/Modules")
   def simulateAllModules(self):
      for m in self.modules:
         m.simulate()
   
   @Timing.timedFunction("Simulate/Ship/Collisions")
   def simulateCollisions(self):
      didLoseModules = False
      for item in self.world.all[:]:
         if item == self or not item.solidFor(self):
            continue
         
         range = Vector.distance(item.position, self.position)
         if abs(range) > 500:
            continue
         
         for module in self.modules[:]:
            radius = Scalar.bound(MODULE_SIZE * 2, (2.0 * Vector.magnitude(item.velocity)), MODULE_SIZE * 10)
            if abs(Vector.magnitude(Vector.offset(item.position, module.absolutePosition()))) < radius:
               self.applyForce(Vector.scale(item.velocity, 2), module.position)

               didLoseModules = True
               self.explodeModule(module)
               
               if item.combatTeam == -1:
                  item.destroyed = True
               
      if not (self.flightComputer in self.modules):
         for m in self.modules:
            self.explodeModule(module)
            
         self.world.addObject(Explosion(self.flightComputer.absolutePosition(), self.velocity, 250))
         self.destroyed = True
         return
      
      if didLoseModules:
         connectedModules = []
         def recurseModules(start):
            for m in self.modules:
               if m in connectedModules:
                  continue
               
               distance = Vector.magnitude(Vector.offset(start.position, m.position))
               if distance < MODULE_SIZE * 1.2:
                  connectedModules.append(m)
                  recurseModules(m)
         
         recurseModules(self.flightComputer)
         
         for m in self.modules[:]:
            if not m in connectedModules:
               self.explodeModule(m)
         
         #self.recalculateModules()
                     
   def explodeModule(self, module):
      if module in self.modules:
         self.modules.remove(module)
         self.world.addObject(Explosion(module.absolutePosition(), self.velocity, 65))
