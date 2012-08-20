
import math
import Timing

def vectorSum(vector):
   if len(vector) == 0:
      return 0

   result = 0.0
   for v in vector:
      result += v

   return result

def vectorDistance(a, b):
   return math.sqrt( (b[0]-a[0])*(b[0]-a[0]) + (b[1]-a[1])*(b[1]-a[1]) )

def vectorAdd(a, b):
   return (a[0] + b[0], a[1] + b[1])
   
def vectorMultiply(a, b):
   return (a[0] * b[0], a[1] * b[1])
   
def vectorScale(vector, scale):
   return (vector[0] * scale, vector[1] * scale)
   
def vectorOffset(a, b):
   return (a[0] - b[0], a[1] - b[1])
   
def vectorSquare(vector):
   return (vector[0]**2, vector[1]**2)
   
def vectorMagnitude(vector):
   return math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])
   
def vectorDirection(vector):
   return math.atan2(vector[1], vector[0])
   
def vectorRotate(vector, angle):
   x, y = vector
   sin = math.sin(angle)
   cos = math.cos(angle)

   return (cos*x - sin*y, sin*x + cos*y)
   
def vectorMidpoint(a, b):
   return ( (a[0]+b[0])/2.0, (a[1]+b[1])/2.0 )
   
def vectorShortestAngleBetween(a, b):
   return math.atan2(math.sin(b - a), math.cos(b - a))
   
def vectorNormalize(vector):
   if magnitude(vector) == 0:
      return (0, 0)
      
   return scale(vector, 1.0 / magnitude(vector))
   
def vectorDot(a, b):
   return sum(multiply(a, b))
   
def vectorScalarProjection(a, b):
   return dot(a, b) / magnitude(b)
   
