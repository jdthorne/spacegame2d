
import math
import Timing

@Timing.timedFunction("Vector/Sum")
def sum(vector):
   if len(vector) == 0:
      return 0

   result = 0.0
   for v in vector:
      result += v

   return result

@Timing.timedFunction("Vector/Distance")
def distance(a, b):
   return math.sqrt( (b[0]-a[0])**2 + (b[1]-a[1])**2 )

@Timing.timedFunction("Vector/Add")
def add(a, b):
   return (a[0] + b[0], a[1] + b[1])
   
@Timing.timedFunction("Vector/Multiply")
def multiply(a, b):
   return (a[0] * b[0], a[1] * b[1])
   
@Timing.timedFunction("Vector/Scale")
def scale(vector, scale):
   return (vector[0] * scale, vector[1] * scale)
   
@Timing.timedFunction("Vector/Offset")
def offset(a, b):
   return (a[0] - b[0], a[1] - b[1])
   
@Timing.timedFunction("Vector/Square")
def square(vector):
   return (vector[0]**2, vector[1]**2)
   
@Timing.timedFunction("Vector/Magnitude")
def magnitude(vector):
   return math.sqrt(vector[0]*vector[0] + vector[1]*vector[1])
   
@Timing.timedFunction("Vector/Direction")
def direction(vector):
   return math.atan2(vector[1], vector[0])
   
@Timing.timedFunction("Vector/ApplyMatrix")
def applyMatrix(vector, matrix):
   x, y = vector
   a, b, c, d = matrix
   return [ a*x + b*y , c*x + d*y ]
   
@Timing.timedFunction("Vector/RotationMatric")
def rotationMatrix(angle):
   return [ math.cos(angle) , -math.sin(angle) , math.sin(angle), math.cos(angle) ]
   
@Timing.timedFunction("Vector/Rotate")
def rotate(vector, angle):
   return applyMatrix(vector, rotationMatrix(angle))
   
@Timing.timedFunction("Vector/Midpoint")
def midpoint(a, b):
   return ( (a[0]+b[0])/2.0, (a[1]+b[1])/2.0 )
   
@Timing.timedFunction("Vector/ShortestAngle")
def shortestAngleBetween(a, b):
   return math.atan2(math.sin(b - a), math.cos(b - a))
   
@Timing.timedFunction("Vector/Normalize")
def normalize(vector):
   if magnitude(vector) == 0:
      return (0, 0)
      
   return scale(vector, 1.0 / magnitude(vector))
   
@Timing.timedFunction("Vector/Dot")
def dot(a, b):
   return sum(multiply(a, b))
   
@Timing.timedFunction("Vector/ScalarProject")
def scalarProjection(a, b):
   return dot(a, b) / magnitude(b)
   
