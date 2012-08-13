
import math

def Sum(vector):
	add = lambda a, b: a + b
	return reduce(add, vector)

def Add(a, b):
	return [ a[i] + b[i] + 0.0 for i in range(len(a)) ]
	
def Multiply(a, b):
	return [ a[i] * b[i] * 1.0 for i in range(len(a)) ]	
	
def Scale(vector, scale):
	return [ element * (scale + 0.0) for element in vector ]
	
def Offset(a, b):
	return [ a[i] - b[i] + 0.0 for i in range(len(a)) ]
	
def Square(vector):
	return [ e*e for e in vector ]
	
def Magnitude(vector):
	return abs(math.sqrt(Sum(Square(vector))))
	
def Direction(vector):
	return math.atan2(vector[1], vector[0])
	
def ApplyMatrix(vector, matrix):
	x, y = vector
	a, b, c, d = matrix
	return [ a*x + b*y , c*x + d*y ]
	
def RotationMatrix(angle):
	return [ math.cos(angle) , -math.sin(angle) , math.sin(angle), math.cos(angle) ]
	
def Rotate(vector, angle):
	return ApplyMatrix(vector, RotationMatrix(angle))
	
def Midpoint(a, b):
	return [ (a[i] + b[i]) / 2.0 for i in range(len(a)) ]
	
def ShortestAngleBetween(a, b):
	return math.atan2(math.sin(b - a), math.cos(b - a))