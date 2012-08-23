
import math

import Sprite
from Scalar import *
from Vector import *

frameOfReference = ([0, 0], 0, None)
vectorsToDraw = []

def displayVector(vector, color="red", scale=1, position=[0, 0]):
   if vectorMagnitude(vector) == 0:
      return

   vector = vectorScale(vector, scale)
   vector = vectorRotate(vector, frameOfReference[1])

   position = vectorRotate(position, frameOfReference[1])
   
   startPoint = vectorAdd(position, frameOfReference[0])
   endPoint = vectorAdd(startPoint, vector)
   
   vectorsToDraw.append( (startPoint, endPoint, color, frameOfReference[2]) )

def draw(ship):
   for startPoint, endPoint, color, forShip in vectorsToDraw:
      if ship == forShip:
         length = vectorDistance(startPoint, endPoint)
         rotation = vectorDirection(vectorOffset(endPoint, startPoint))
         scale = length / 200.0

         Sprite.draw("vector-%s" % (color,), position=startPoint, scale=scale, rotation=rotation)
   

def clear():
   del vectorsToDraw[:]
