
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
      self.analysis = Analysis(self.ship)
      self.currentStatus = (0, "")
      
   def run(self):      
      if self.engineCount != len(self.ship.engines()):
         self.analysis = Analysis(self.ship)
      
      self.clearEngines()

      self.acquireTarget()
      
      if self.target != None:
         self.rotateToFaceTarget()
         self.thrustToTargetRadius()
         self.fireWeaponsIfPossible()
   
   def status(self):
      if self.target is None:
         return (0.0, "ready")
      else:
         return self.currentStatus

   # ========== HIGH-LEVEL CONTROLS =============
   def acquireTarget(self):
      closestTarget = None
      closestRange = 0
      for target in self.ship.sensors().scan():
         if (target.combatTeam() != -1) and (target.combatTeam() != self.ship.combatTeam()):
            range = (abs(vectorDirection(target.vector())) * 600) + abs(vectorMagnitude(target.vector()))
         
            if (closestTarget == None) or (range < closestRange):
               closestRange = range
               closestTarget = target
         
      self.target = closestTarget
   
   def rotateToFaceTarget(self):
      angularDistance = vectorDirection(Autolib.interceptVector(self.target))
      angularSpeed = self.ship.spin()
      
      power = Autolib.powerForSmoothApproach(angularDistance, angularSpeed,
                                        self.analysis.maxPositiveDizzy, 
                                          self.analysis.maxNegativeDizzy)
         
      self.powerEngines(power, self.analysis.positiveDizzyEngines, self.analysis.negativeDizzyEngines)
      self.currentStatus = (0.2, "acquiring target")
   
   
   def thrustToTargetRadius(self):
      if abs(vectorDirection(self.target.vector())) < 0.5:
         distance = vectorMagnitude(self.target.vector()) - (Misc.WEAPON_RANGE / 2.0)
         speed = vectorScalarProjection(self.target.velocity(), [-1, 0])
         
         maxTowardAcceleration = self.analysis.maxRemainingForwardAcceleration()
         maxAwayAcceleration = self.analysis.maxRemainingReverseAcceleration()
         
         power = Autolib.powerForSmoothApproach(distance, speed, 
                                           maxTowardAcceleration, 
                                           maxAwayAcceleration)
   
         self.powerEngines(power, self.analysis.forwardEngines, self.analysis.reverseEngines)
         self.currentStatus = (0.5, "approaching")
      
   def fireWeaponsIfPossible(self):
      intercept = Autolib.interceptVector(self.target)
      direction = abs(vectorDirection(intercept))
      range = abs(vectorMagnitude(intercept))
      
      if direction < 0.1 and range < Misc.WEAPON_RANGE:
         self.weaponsEngaged = True

      if direction > 0.3 or range > Misc.WEAPON_RANGE * 2.5:
         self.weaponsEngaged = False
         
      if self.weaponsEngaged:
         self.currentStatus = (1.0, "firing")
         self.fireAllWeapons()

   # =============== LOW-LEVEL COMMANDS ===============
   
   def clearEngines(self):
      for e in self.ship.engines():
         e.setPower(0)
         
   def powerEngines(self, power, positiveEngines, negativeEngines):
      for e in positiveEngines:
         e.setPower(e.power() + power)
         
      for e in negativeEngines:
         e.setPower(e.power() - power)
         
   def fireAllWeapons(self):
      for w in self.ship.weapons():
         w.fire()

         
      
      
