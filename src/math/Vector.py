
from math import sqrt, cos, sin, atan2
import Timing

@Timing.timedFunction
def vectorSum(vector):
   if len(vector) == 0:
      return 0

   result = 0.0
   for v in vector:
      result += v

   return result

@Timing.timedFunction
def vectorDistance(a, b):
   return sqrt( (b[0]-a[0])*(b[0]-a[0]) + (b[1]-a[1])*(b[1]-a[1]) )

@Timing.timedFunction
def vectorAdd(a, b):
   return (a[0] + b[0], a[1] + b[1])
   
@Timing.timedFunction
def vectorMultiply(a, b):
   return (a[0] * b[0], a[1] * b[1])
   
@Timing.timedFunction
def vectorScale(vector, scale):
   return (vector[0] * scale, vector[1] * scale)
   
@Timing.timedFunction
def vectorOffset(a, b):
   return (a[0] - b[0], a[1] - b[1])
   
@Timing.timedFunction
def vectorSquare(vector):
   return (vector[0]**2, vector[1]**2)
   
@Timing.timedFunction
def vectorMagnitude(vector):
   return sqrt(vector[0]*vector[0] + vector[1]*vector[1])
   
@Timing.timedFunction
def vectorDirection(vector):
   return atan2(vector[1], vector[0])
   
@Timing.timedFunction
def vectorRotate(vector, angle):
   x, y = vector
   sinv = sin(angle)
   cosv = cos(angle)

   return (cosv*x - sinv*y, sinv*x + cosv*y)
   
@Timing.timedFunction
def vectorMidpoint(a, b):
   return ( (a[0]+b[0])/2.0, (a[1]+b[1])/2.0 )
   
@Timing.timedFunction
def vectorShortestAngleBetween(a, b):
   return atan2(sin(b - a), cos(b - a))
   
@Timing.timedFunction
def vectorNormalize(vector):
   if vectorMagnitude(vector) == 0:
      return (0, 0)
      
   return vectorScale(vector, 1.0 / vectorMagnitude(vector))
   
@Timing.timedFunction
def vectorDot(a, b):
   return vectorSum(vectorMultiply(a, b))
   
@Timing.timedFunction
def vectorScalarProjection(a, b):
   return vectorDot(a, b) / vectorMagnitude(b)
   
