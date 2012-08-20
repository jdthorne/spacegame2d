
import math

import HUD
import Scalar
from Vector import *

class Analysis:
   def __init__(self, ship):
      self.ship = ship
      
      self.zeroDizzyEngines = [ e for e in ship.engines() if e.dizzy() == 0 ]
      self.positiveDizzyEngines = [ e for e in ship.engines() if e.dizzy() > 0 ]
      self.negativeDizzyEngines = [ e for e in ship.engines() if e.dizzy() < 0 ]
   
      self.maxPositiveDizzy = vectorSum([ e.dizzy() for e in self.positiveDizzyEngines ])
      self.maxNegativeDizzy = vectorSum([ e.dizzy() for e in self.positiveDizzyEngines ])

      self.forwardEngines = [ e for e in ship.engines() if e.thrustVector()[0] > 0 ]
      self.reverseEngines = [ e for e in ship.engines() if e.thrustVector()[0] < 0 ]
      
      self.maxForwardAcceleration = vectorSum([ e.acceleration()[0] for e in self.forwardEngines ])
      self.maxReverseAcceleration = vectorSum([ e.acceleration()[0] for e in self.reverseEngines ])
   
   def maxRemainingForwardAcceleration(self):
      return vectorSum( [e.acceleration()[0] * (1.0 - e.power()) for e in self.forwardEngines] )
      
   def maxRemainingReverseAcceleration(self):
      return vectorSum( [e.acceleration()[0] * (1.0 - e.power()) for e in self.reverseEngines] )
         
         
class Autopilot:
   def __init__(self, ship):
      self.target = None
      self.ship = ship
      
      self.weaponsEngaged = False
      self.engineCount = len(self.ship.engines())
      self.analysis = Analysis(self.ship)
      
   def run(self):      
      if self.engineCount != len(self.ship.engines()):
         self.analysis = Analysis(self.ship)
      
      self.clearEngines()
      self.acquireTarget()
      if self.target != None:
         self.spin()
         self.thrustToTarget()
         self.fireIfAble()
      
   # ========== HIGH-LEVEL CONTROLS =============
   def acquireTarget(self):
      closestTarget = None
      closestRange = 0
      for target in self.ship.sensors().scan():
         if (target.combatTeam() != -1) and (target.combatTeam() != self.ship.combatTeam()):
            range = (abs(Vector.direction(target.vector())) * 600) + abs(vectorMagnitude(target.vector()))
         
            if (closestTarget == None) or (range < closestRange):
               closestRange = range
               closestTarget = target
         
      self.target = closestTarget
   
   def spin(self):
      if self.ship.spin() < 0.2:
         self.powerEngines(1.0, self.analysis.positiveDizzyEngines, [])
      
   def thrustToTarget(self):
      direction = Vector.direction(self.target.vector())
      if abs(direction) < 0.2:
         self.powerEngines(1.0, self.analysis.forwardEngines)
      elif abs(direction) > math.pi - 0.2:
         self.powerEngines(-1.0, [], self.analysis.reverseEngines)

   def fireIfAble(self):
      spinSpeed = abs(self.ship.spin() * 0.51)

      for target in self.ship.sensors().scan():
         direction = abs(Vector.direction(self.target.vector()))
         range = abs(vectorMagnitude(self.target.vector()))

         if direction < spinSpeed and range < 2500:
            self.fireAllWeapons()
            return

   # =============== LOW-LEVEL COMMANDS ===============
   
   def clearEngines(self):
      for e in self.ship.engines():
         e.setPower(0)
         
   def powerEngines(self, power, positiveEngines, negativeEngines=[]):
      for e in positiveEngines:
         e.setPower(e.power() + power)
         
      for e in negativeEngines:
         e.setPower(e.power() - power)
         
   def fireAllWeapons(self):
      for w in self.ship.weapons():
         w.fire()

         
      
      
