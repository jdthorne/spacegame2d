
import math

import HUD
import Scalar
from Vector import *

def calculatePowerLevelForSmoothApproach(distance, currentSpeed, maxPositiveAcceleration, maxNegativeAcceleration, log=False):
   if abs(distance) < 0.000001:
      return 0.0

   #if distance < 0 and abs(distance) < abs(currentSpeed * 4.0):
   #   return 0.0

   targetAcceleration = -(currentSpeed**2) / (2*distance)
   maxAppropriateAcceleration = maxNegativeAcceleration if distance < 0 else maxPositiveAcceleration
   maxAppropriateBraking = maxPositiveAcceleration if distance < 0 else maxNegativeAcceleration
   
   info = "[ Distance = %07.2f, Speed = %.5f, Target Acc = %.5f, Max Braking = %.5f ]" % (distance, currentSpeed, targetAcceleration, maxAppropriateBraking)
   
   if log:
      print info, 

   # Moving away from the target - use full power towards it
   if Scalar.sign(currentSpeed) != Scalar.sign(distance):
      if log:
         print "BURN (moving away)"
   
      return 1.0 * Scalar.sign(distance)
   
   # We have lots of time to brake, so let's accelerate instead
   elif abs(targetAcceleration) < abs(maxAppropriateBraking * 0.75):
      if log:
         print "BURN (have time)"
   
      return 1.0 * Scalar.sign(distance)
      
   # We should brake now!
   if log:
      print "BRAKE"
   return abs(targetAcceleration / maxAppropriateBraking) * -Scalar.sign(distance)
   
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
         self.rotateToFaceTarget()
         self.thrustToTargetRadius()
         self.fireWeaponsIfPossible()
   
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
   
   def rotateToFaceTarget(self):
      angularDistance = Vector.direction(self.target.vector())
      angularSpeed = self.ship.spin()
      
      power = calculatePowerLevelForSmoothApproach(angularDistance, angularSpeed,
                                        self.analysis.maxPositiveDizzy, 
                                          self.analysis.maxNegativeDizzy,
                                          log=False)
         
      self.powerEngines(power, self.analysis.positiveDizzyEngines, self.analysis.negativeDizzyEngines)
   
   
   def thrustToTargetRadius(self):
      if abs(Vector.direction(self.target.vector())) < 0.5:
         distance = vectorMagnitude(self.target.vector()) - 900
         speed = vectorScalarProjection(self.target.velocity(), [-1, 0])
         
         maxTowardAcceleration = self.analysis.maxRemainingForwardAcceleration()
         maxAwayAcceleration = self.analysis.maxRemainingReverseAcceleration()
         
         power = calculatePowerLevelForSmoothApproach(distance, speed, 
                                           maxTowardAcceleration, 
                                           maxAwayAcceleration,
                                           log=False)
   
         self.powerEngines(power, self.analysis.forwardEngines, self.analysis.reverseEngines)
      
   def fireWeaponsIfPossible(self):
      direction = abs(Vector.direction(self.target.vector()))
      range = abs(vectorMagnitude(self.target.vector()))
      
      if direction < 0.1 and range < 2500:
         self.weaponsEngaged = True

      if direction > 0.3 or range > 6000:
         self.weaponsEngaged = False
         
      if self.weaponsEngaged:
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

         
      
      
