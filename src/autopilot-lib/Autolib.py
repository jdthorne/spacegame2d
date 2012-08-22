import Scalar
import Misc
import HUD
from Vector import *

def interceptVector(target):
   distance = vectorMagnitude(target.vector())

   interceptSpeed = Misc.BULLET_SPEED

   timeToIntercept = distance / interceptSpeed

   targetDisplacement = vectorScale(target.velocity(), timeToIntercept)
   #HUD.displayVector(targetDisplacement, position=target.vector(), color="red")

   newPosition = vectorAdd(target.vector(), targetDisplacement)
   #HUD.displayVector(newPosition, color="green")
   return newPosition

def powerForSmoothApproach(distance, currentSpeed, maxPositiveAcceleration, maxNegativeAcceleration):
   if abs(distance) < 0.000001:
      return 0.0

   if maxPositiveAcceleration == 0 or maxNegativeAcceleration == 0:
      return 0.0

   #if distance < 0 and abs(distance) < abs(currentSpeed * 4.0):
   #   return 0.0

   targetAcceleration = -(currentSpeed**2) / (2*distance)
   maxAppropriateAcceleration = maxNegativeAcceleration if distance < 0 else maxPositiveAcceleration
   maxAppropriateBraking = maxPositiveAcceleration if distance < 0 else maxNegativeAcceleration
   
   # Moving away from the target - use full power towards it
   if Scalar.sign(currentSpeed) != Scalar.sign(distance):
      return 1.0 * Scalar.sign(distance)
   
   # We have lots of time to brake, so let's accelerate instead
   elif abs(targetAcceleration) < abs(maxAppropriateBraking * 0.75):
      return 1.0 * Scalar.sign(distance)
      
   # We should brake now!
   return abs(targetAcceleration / maxAppropriateBraking) * -Scalar.sign(distance)
