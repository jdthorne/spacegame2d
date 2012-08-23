
import math

import HUD
from Scalar import *
import Misc
import Autolib
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
      self.targetCount = 0
      self.analysis = Analysis(self.ship)
      
   def run(self):      
      if self.engineCount != len(self.ship.engines()):
         self.analysis = Analysis(self.ship)
      
      self.clearEngines()
      self.acquireTarget()
      self.spin()
      self.thrustToTarget()
      self.fireIfAble()

   def status(self):
      if self.targetCount > 0:
         return (1.0, "%d targets" % (self.targetCount,))
      elif self.ship.spin() < 0.2:
         return (0.5, "spinning up")
      else:
         return (0.2, "ready")
         
      
   # ========== HIGH-LEVEL CONTROLS =============
   def acquireTarget(self):
      closestTarget = None
      closestRange = 0

      self.targets = []

      for target in self.ship.sensors().scan():
         if (target.combatTeam() != -1) and (target.combatTeam() != self.ship.combatTeam()):
            distance = vectorMagnitude(target.vector())

            if distance < Misc.WEAPON_RANGE:
               self.targets.append(target)
         
            if (closestTarget == None) or (distance < closestRange):
               closestRange = distance
               closestTarget = target
         
      self.targetCount = len(self.targets)
      self.target = closestTarget
   
   def spin(self):
      if self.ship.spin() < 0.2:
         self.powerEngines(1.0, self.analysis.positiveDizzyEngines, [])

      elif self.ship.spin() > 0.4:
         self.powerEngines(-1.0, [], self.analysis.negativeDizzyEngines)
      
   def thrustToTarget(self):
      if self.target == None:
         return

      if self.targetCount < 4:
         # We're cool - ATTACK
         targetDirection = vectorDirection(self.target.vector())

      else:
         # Run away!
         averageTargetVector = (0, 0)
         for target in self.targets:
            averageTargetVector = vectorAdd(target.vector(), averageTargetVector)

         targetDirection = vectorDirection(vectorScale(averageTargetVector, -1))

      if abs(targetDirection) < 0.6:
         self.powerEngines(1.0, self.analysis.forwardEngines)
      elif abs(targetDirection) > math.pi - 0.6:
         self.powerEngines(-1.0, [], self.analysis.reverseEngines)



   def fireIfAble(self):
      spinSpeed = abs(self.ship.spin() * 0.51)

      for target in self.targets:
         vector = Autolib.interceptVector(target)

         direction = abs(vectorDirection(vector))

         if direction < spinSpeed:
            self.fireAtTarget()
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
         
   def fireAtTarget(self):
      weaponsToFire = len(self.ship.weapons()) / scalarBound(1, self.targetCount, 3)
      for w in self.ship.weapons():
         if w.ready():
            w.fire()
            weaponsToFire -= 1

         if weaponsToFire <= 0:
            return

         
      
      
