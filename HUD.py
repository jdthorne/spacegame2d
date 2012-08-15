
import wx
import math

import Scalar
import Vector

frameOfReference = ([0, 0], 0)
vectorsToDraw = []

def DisplayVector(vector, color=wx.RED, scale=1, position=[0, 0]):
	if Vector.Magnitude(vector) == 0:
		return

	vector = Vector.Scale(vector, scale)
	vector = Vector.Rotate(vector, frameOfReference[1])
	
	startPoint = Vector.Add(position, frameOfReference[0])
	endPoint = Vector.Add(startPoint, vector)
	
	arrowVector = Vector.Scale(Vector.Normalize(vector), 8)

	t1 = Vector.Add(endPoint, Vector.Rotate(arrowVector, math.pi * 0.90))
	t2 = Vector.Add(endPoint, Vector.Rotate(arrowVector, math.pi * -0.90))
		
	vectorsToDraw.append( (startPoint, endPoint, t1, t2, color) )

def Draw(dc):
	
	for startPoint, endPoint, t1, t2, color in vectorsToDraw:
		dc.SetPen(wx.Pen(color, 2))
		
		x1, y1 = startPoint
		x2, y2 = endPoint
		
		dc.DrawLine(x1, 720-y1, x2, 720-y2)

		t1x, t1y = t1
		dc.DrawLine(t1x, 720-t1y, x2, 720-y2)

		t2x, t2y = t2
		dc.DrawLine(t2x, 720-t2y, x2, 720-y2)
	
	del vectorsToDraw[:]
	