
import math

import HUD
from Vector import *
from Scalar import *
import World
import Misc

import App
import Modules
import ShipControls
import Event
import Physics
import Timing
import random

nextShipId = 0

SHIP_SIZE = 1200.0

class Ship(Physics.RigidBody):
   def __init__(self, definition, position, rotation, velocity, combatTeam):
      Physics.RigidBody.__init__(self, position)

      global nextShipId
      self.id = nextShipId
      nextShipId += 1

      self.status = (0, "")
      self.jumpComplete = False

      self.ftlTime = 25
      self.name = definition.name
      self.combatTeam = combatTeam
      self.exciting = True
      self.world = App.world
      self.rotation = rotation
      self.isShip = True
      self.availableDeflectorPower = 1000.0
      self.velocity = velocity

      self.damaged = False
      self.hasTakenDamage = False

      self.onLayoutChanged = Event.Event(self)
      
      self.flightComputer = None
      self.modules = []

      self.moduleOffset = (0, 0)
      
      for moduleType, x, y in allModules(definition.design):
         #x *= Misc.MODULE_SIZE
         #y *= Misc.MODULE_SIZE
         
         self.installModule(moduleType, (x, y))
         
      self.engines = [m for m in self.modules if isinstance(m, Modules.Engine)]
      self.weapons = [r for r in self.modules if isinstance(r, Modules.PlasmaCannon)]

      self.installAutopilot(definition.autopilot)

      random.shuffle(self.engines)
      random.shuffle(self.weapons)
      
      self.moduleOffset = (0, 0)
      self.recalculateModules()

   def installAutopilot(self, autopilot):
      self.flightComputer.installAutopilot(autopilot)

   def installModule(self, moduleType, modulePosition):
      position = vectorScale(modulePosition, Misc.MODULE_SIZE)
      position = vectorOffset(position, self.moduleOffset)

      for module in self.modules:
         if vectorDistance(module.position, position) < Misc.MODULE_SIZE / 2:
            if module is self.flightComputer:
               return

            elif module.installType == moduleType:
               return

            self.explodeModule(module, boom=False)

      x, y = position
      module = None

      if moduleType == "C":
         module = Modules.FlightComputer(self, [x, y], None)
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
      
      if module != None:
         module.installType = moduleType
         module.installPosition = modulePosition
         self.modules.append(module)

      self.onLayoutChanged()

   def design(self):
      min, max = vectorBounds( [m.installPosition for m in self.modules] )
      
      str = ""
      for y in range(int(min[1]), int(max[1]+1)):
         for x in range(int(min[0]), int(max[0]+1)):

            installType = " "
            for module in self.modules:
               if module.installPosition == (x, y):
                  installType = module.installType
                  found = True
                  break

            str += installType

         str += "\n"

      return str


   def __hash__(self):
      return self.id
      
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
      self.moduleOffset = vectorAdd(self.moduleOffset, move)
      
      # Recalculate moment of inertia
      def massRadiusSquared(module):
         radius = vectorMagnitude(module.position)
         return module.mass * radius * radius
         
      result = vectorSum([massRadiusSquared(m) for m in self.modules])
      if result < 1.0:
         return 1.0
         
      self.calculatedMomentOfInertia = result

      # Calculate other stats
      self.maxDeflectorPower = 1.0 + len([ m for m in self.modules if isinstance(m, Modules.Deflector) ])
      self.collisionRadius = max([ vectorMagnitude(m.position) for m in self.modules ]) + Misc.MODULE_SIZE

   @Timing.timedFunction
   def simulate(self):
      Physics.RigidBody.simulate(self)

      HUD.frameOfReference = (self.position, self.rotation, self)
      
      self.simulateAllModules()
      self.simulateWorldEffects()
      
   @Timing.timedFunction
   def simulateAllModules(self):
      for m in self.modules:
         m.simulate()


   @Timing.timedFunction
   def simulateWorldEffects(self):
      if self.ftlTime > 0:
         self.ftlTime -= 1

      self.damaged = False

      powerupTime = 5.0 * 90.0

      self.availableDeflectorPower += self.maxDeflectorPower / powerupTime
      self.availableDeflectorPower = scalarBound(0, self.availableDeflectorPower, self.maxDeflectorPower)
      self.currentDeflectorPower = self.availableDeflectorPower / self.maxDeflectorPower

      for item in self.world.all:
         if (item is self) or (not item.solidFor(self)):
            continue

         distance = vectorDistance(item.position, self.position)
         if abs(distance) < SHIP_SIZE:
            self.simulateDeflectors(item, distance)

         if abs(distance) < self.collisionRadius:
            self.simulateCollisions(item)

      if self.damaged:
         self.simulateDamage()
         self.onLayoutChanged()

   def simulateDeflectors(self, item, distance):
      if self.availableDeflectorPower < 0.02:
         return

      if distance < 1:
         return

      delta = vectorDistance(item.velocity, self.velocity)
      if delta < 0.01:
         item.velocity = self.velocity
         return

      power = (SHIP_SIZE - distance) / SHIP_SIZE
      power = power * power * (self.availableDeflectorPower / self.maxDeflectorPower)

      mix = power * 2
      item.velocity = vectorAdd(vectorScale(item.velocity, 1.0-mix), vectorScale(self.velocity, mix))

      self.availableDeflectorPower -= (power * delta * 0.002)

   def simulateCollisions(self, item):
      radius = (2.0 * vectorMagnitude(item.velocity))
      radius = scalarBound(Misc.MODULE_SIZE * 2, radius, Misc.MODULE_SIZE * 10)

      for module in self.modules:
         distance = abs(vectorDistance(item.position, module.absolutePosition()))
         if distance < radius:
            self.applyForce(vectorScale(item.velocity, 2), module.position)

            self.damaged = True
            self.explodeModule(module)
            
            item.collide()

   @Timing.timedFunction
   def simulateDamage(self):
      connectedModules = []
      def recurseModules(start):
         for m in self.modules:
            if m in connectedModules:
               continue
            
            distance = vectorMagnitude(vectorOffset(start.position, m.position))
            if distance < Misc.MODULE_SIZE * 1.2:
               connectedModules.append(m)
               recurseModules(m)
      
      recurseModules(self.flightComputer)
      
      for m in self.modules[:]:
         if not m in connectedModules:
            self.explodeModule(m)
      
      #self.recalculateModules()

   def explodeModule(self, module, boom=True):
      self.hasTakenDamage = True
      if not (module in self.modules):
         return

      self.modules.remove(module)

      if module is self.flightComputer:
         self.destroy()

      if module in self.weapons:
         self.weapons.remove(module)
      if module in self.engines:
         self.engines.remove(module)

      if boom:
         self.world.addObject(Misc.Explosion(module.absolutePosition(), self.velocity, 65))

   def collide(self):
      # Ships handle their own collisions
      return

   def destroy(self):
      self.world.addObject(Misc.Explosion(self.position, 
                                          self.velocity, 
                                          125 + (15 * len(self.modules))))
      for module in self.modules:
         self.explodeModule(module)

      Physics.RigidBody.destroy(self)



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
   
