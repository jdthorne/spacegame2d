
import math

import HUD
from Vector import *
import Scalar
import World
import Misc

import Modules
import ShipControls
import Physics
import Cache
import Timing

MODULE_SIZE = 40

class Ship(Physics.RigidBody):
   def __init__(self, design, autopilot, position, rotation, world, fleetId):
      Physics.RigidBody.__init__(self, position)
      
      self.combatTeam = fleetId
      self.exciting = True
      self.world = world
      self.rotation = rotation
      self.isShip = True
      self.availableDeflectorPower = 1000.0
      
      self.flightComputer = None
      self.modules = []
      
      for moduleType, x, y in allModules(design):
         x *= MODULE_SIZE
         y *= MODULE_SIZE
         module = None
         
         if moduleType == "C":
            module = Modules.FlightComputer(self, [x, y], autopilot)
            self.flightComputer = module
         elif moduleType == "S":
            module = Modules.Structure(self, [x, y])
         elif moduleType == "<":
            module = Modules.Engine(self, [x, y], [6, 0])
         elif moduleType == ">":
            module = Modules.Engine(self, [x, y], [-6, 0])
         elif moduleType == "]":
            module = Modules.Engine(self, [x, y], [-2, 0])
         elif moduleType == "[":
            module = Modules.Engine(self, [x, y], [2, 0])
         elif moduleType == "P":
            module = Modules.PlasmaCannon(self, [x, y])
         elif moduleType == "D":
            module = Modules.Deflector(self, [x, y])
         
         self.modules.append(module)
         
      self.engines = [m for m in self.modules if isinstance(m, Modules.Engine)]
      self.weapons = [r for r in self.modules if isinstance(r, Modules.PlasmaCannon)]
      
      self.recalculateModules()
      
   def scanForTargets(self):
      return [ t for t in self.world.scan() if not (t is self) ]

   def centerOfMass(self):
      x = vectorSum([m.mass * m.position[0] for m in self.modules]) / self.mass()
      y = vectorSum([m.mass * m.position[1] for m in self.modules]) / self.mass()
      
      return (x, y)

   def mass(self):
      return self.calculatedMass
      
   def momentOfInertia(self):
      return self.calculatedMomentOfInertia
      
   def recalculateModules(self):
      # Recalculate mass
      self.calculatedMass = vectorSum([m.mass for m in self.modules])
      
      # Move to center of mass
      move = self.centerOfMass()      
      for m in self.modules:
         m.position = vectorOffset(m.position, move)
         
      self.position = vectorAdd(self.position, move)
      
      # Recalculate moment of inertia
      def massRadiusSquared(module):
         radius = vectorMagnitude(module.position)
         return module.mass * radius * radius
         
      result = vectorSum([massRadiusSquared(m) for m in self.modules])
      if result < 1.0:
         return 1.0
         
      self.calculatedMomentOfInertia = result

      # Calculate other stats
      self.maxDeflectorPower = len([ m for m in self.modules if isinstance(m, Modules.Deflector) ])
      self.collisionRadius = max([ vectorMagnitude(m.position) for m in self.modules ]) + MODULE_SIZE

   @Timing.timedFunction
   def simulate(self):
      Physics.RigidBody.simulate(self)
      HUD.frameOfReference = (self.position, self.rotation)
      
      self.simulateAllModules()
      self.simulateWorldEffects()
      
   @Timing.timedFunction
   def simulateAllModules(self):
      for m in self.modules:
         m.simulate()


   @Timing.timedFunction
   def simulateWorldEffects(self):
      self.damaged = False
      self.availableDeflectorPower = Scalar.bound(0, self.availableDeflectorPower, self.maxDeflectorPower)
      self.currentDeflectorPower = self.availableDeflectorPower / self.maxDeflectorPower

      for item in self.world.all:
         if (item is self) or (not item.solidFor(self)):
            continue

         distance = vectorDistance(item.position, self.position)
         if abs(distance) < 900.0:
            self.simulateDeflectors(item, distance)

         if abs(distance) < self.collisionRadius:
            self.simulateCollisions(item)

      if self.damaged:
         self.simulateDamage()

   def simulateDeflectors(self, item, distance):
      if self.availableDeflectorPower < 0.02:
         return

      if distance < 1:
         return

      delta = vectorDistance(item.velocity, self.velocity)
      if delta < 0.01:
         item.velocity = self.velocity
         return

      power = (900.0 - distance) / 900.0
      power = power * power * (self.availableDeflectorPower / self.maxDeflectorPower)

      mix = power
      item.velocity = vectorAdd(vectorScale(item.velocity, 1.0-mix), vectorScale(self.velocity, mix))

      self.availableDeflectorPower -= (power * delta * 0.004)

   def simulateCollisions(self, item):
      radius = (2.0 * vectorMagnitude(item.velocity))
      radius = Scalar.bound(MODULE_SIZE * 2, radius, MODULE_SIZE * 10)

      for module in self.modules:
         distance = abs(vectorDistance(item.position, module.absolutePosition()))
         if distance < radius:
            self.applyForce(vectorScale(item.velocity, 2), module.position)

            self.damaged = True
            self.explodeModule(module)
            
            if item.combatTeam == -1:
               item.destroyed = True
               return

   @Timing.timedFunction
   def simulateDamage(self):
      if self.destroyed:
         for module in self.modules:
            self.explodeModule(module)
            
         self.world.addObject(Misc.Explosion(self.flightComputer.absolutePosition(), 
                                             self.velocity, 
                                             250))
         return
   
      connectedModules = []
      def recurseModules(start):
         for m in self.modules:
            if m in connectedModules:
               continue
            
            distance = vectorMagnitude(vectorOffset(start.position, m.position))
            if distance < MODULE_SIZE * 1.2:
               connectedModules.append(m)
               recurseModules(m)
      
      recurseModules(self.flightComputer)
      
      for m in self.modules[:]:
         if not m in connectedModules:
            self.explodeModule(m)
      
      #self.recalculateModules()

                     
   def explodeModule(self, module):
      if not (module in self.modules):
         return

      if module is self.flightComputer:
         self.destroyed = True

      self.modules.remove(module)
      self.world.addObject(Misc.Explosion(module.absolutePosition(), self.velocity, 65))



def allModules(design):
   # Break the design into modules
   modules = []
   
   y = 0
   for line in design.split("\n"):
      x = 0
      for char in line:
         if char != " ":
            modules.append( (char, x, y) )
         x += 1
      
      y += 1
   
   # Find the computer      
   computer = [ m for m in modules if m[0] == "C" ][0]
   dx, dy = computer[1], computer[2]
   
   # Offset the modules
   modules = [ (type, x - dx, y - dy) for type, x, y in modules ]
   
   return modules
   
