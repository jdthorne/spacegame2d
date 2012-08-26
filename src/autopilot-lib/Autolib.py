from Scalar import *
import Misc
import HUD
from Vector import *

def interceptVector(target):
   distance = vectorMagnitude(target.vector())

   interceptSpeed = Misc.BULLET_SPEED
   timeToIntercept = distance / interceptSpeed

   targetDisplacement = vectorScale(target.velocity(), timeToIntercept)

   newPosition = vectorAdd(target.vector(), targetDisplacement)
   return newPosition

def powerForSmoothApproach(distance, currentSpeed, maxPositiveAcceleration, maxNegativeAcceleration):
   if abs(distance) < 0.000001:
      return 0.0

   if maxPositiveAcceleration == 0 or maxNegativeAcceleration == 0:
      return 0.0

   targetAcceleration = -(currentSpeed**2) / (2*distance)
   maxAppropriateAcceleration = maxNegativeAcceleration if distance < 0 else maxPositiveAcceleration
   maxAppropriateBraking = maxPositiveAcceleration if distance < 0 else maxNegativeAcceleration
   
   # Moving away from the target - use full power towards it
   if scalarSign(currentSpeed) != scalarSign(distance):
      return 1.0 * scalarSign(distance)
   
   # We have lots of time to brake, so let's accelerate instead
   elif abs(targetAcceleration) < abs(maxAppropriateBraking * 0.75):
      return 1.0 * scalarSign(distance)
      
   # We should brake now!
   return abs(targetAcceleration / maxAppropriateBraking) * -scalarSign(distance)
