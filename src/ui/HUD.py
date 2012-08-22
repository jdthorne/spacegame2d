
import math

import Scalar
from Vector import *

frameOfReference = ([0, 0], 0)
vectorsToDraw = []

def displayVector(vector, color=(255,0,0), scale=1, position=[0, 0]):
   if Vector.Magnitude(vector) == 0:
      return

   vector = vectorScale(vector, scale)
   vector = Vector.Rotate(vector, frameOfReference[1])
   
   startPoint = Vector.Add(position, frameOfReference[0])
   endPoint = Vector.Add(startPoint, vector)
   
   arrowVector = vectorScale(Vector.Normalize(vector), 8)

   t1 = Vector.Add(endPoint, Vector.Rotate(arrowVector, math.pi * 0.90))
   t2 = Vector.Add(endPoint, Vector.Rotate(arrowVector, math.pi * -0.90))
      
   vectorsToDraw.append( (startPoint, endPoint, t1, t2, color) )

def draw(dc):
   
   def widthOfVector(id):
      return 1 + (id * 2)
   
   vectorId = 0
   for startPoint, endPoint, t1, t2, color in vectorsToDraw:
      dc.SetPen(wx.Pen(color, widthOfVector(len(vectorsToDraw) - vectorId) ))
      
      x1, y1 = startPoint
      x2, y2 = endPoint
      
      dc.DrawLine(x1, 720-y1, x2, 720-y2)

      t1x, t1y = t1
      dc.DrawLine(t1x, 720-t1y, x2, 720-y2)

      t2x, t2y = t2
      dc.DrawLine(t2x, 720-t2y, x2, 720-y2)
      
      vectorId += 1
   
   del vectorsToDraw[:]