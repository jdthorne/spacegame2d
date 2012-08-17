
import math

import HUD
import Scalar
import Vector
import Timing

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
      self.zeroDizzyEngines = [ e for e in ship.engines() if e.dizzy() == 0 ]
      self.positiveDizzyEngines = [ e for e in ship.engines() if e.dizzy() > 0 ]
      self.negativeDizzyEngines = [ e for e in ship.engines() if e.dizzy() < 0 ]
   
      self.maxPositiveDizzy = Vector.sum([ e.dizzy() for e in self.positiveDizzyEngines ])
      self.maxNegativeDizzy = Vector.sum([ e.dizzy() for e in self.positiveDizzyEngines ])
      
      self.forwardEngines = [ e for e in self.zeroDizzyEngines if e.thrustVector()[0] > 0 ]
      self.reverseEngines = [ e for e in self.zeroDizzyEngines if e.thrustVector()[0] < 0 ]
      
      self.maxForwardAcceleration = Vector.sum([ e.acceleration()[0] for e in self.forwardEngines ])
      self.maxReverseAcceleration = Vector.sum([ e.acceleration()[0] for e in self.reverseEngines ])
         
class Autopilot:
   def __init__(self, ship):
      self.target = None
      self.ship = ship
      
      self.weaponsEngaged = False
      self.engineCount = len(self.ship.engines())
      self.analysis = Analysis(self.ship)
      
   @Timing.timedFunction("Simulate/Ship/Autopilot/Run")
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
      if self.target != None and (not self.target.destroyed):
         return
         
      closestTarget = None
      closestRange = 0
      for target in self.ship.sensors().scan():
         if (target.combatTeam() != -1) and (target.combatTeam() != self.ship.combatTeam()):
            range = abs(Vector.direction(target.vector()))
         
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
      distance = Vector.magnitude(self.target.vector()) - 400
      speed = Vector.scalarProjection(self.target.velocity(), [-1, 0])
      
      maxTowardAcceleration = self.analysis.maxForwardAcceleration
      maxAwayAcceleration = self.analysis.maxReverseAcceleration
      
      power = calculatePowerLevelForSmoothApproach(distance, speed, 
                                        maxTowardAcceleration, 
                                        maxAwayAcceleration,
                                        log=False)

      self.powerEngines(power, self.analysis.forwardEngines, self.analysis.reverseEngines)
      
   def fireWeaponsIfPossible(self):
      if abs(Vector.direction(self.target.vector())) < 0.1:
         self.weaponsEngaged = True

      if abs(Vector.direction(self.target.vector())) > 0.3:
         self.weaponsEngaged = False
         
      if self.weaponsEngaged:
         self.fireAllWeapons()

   # =============== LOW-LEVEL COMMANDS ===============
   
   def clearEngines(self):
      for e in self.ship.engines():
         e.setPower(0)
         
   def powerEngines(self, power, positiveEngines, negativeEngines):
      for e in positiveEngines:
         e.setPower(power)
         
      for e in negativeEngines:
         e.setPower(-power)
         
   def fireAllWeapons(self):
      for w in self.ship.weapons():
         w.fire()

         
      
      
