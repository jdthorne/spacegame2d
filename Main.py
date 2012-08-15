#!/opt/local/bin/python

import HUD
import Ship
import wx
import World
import Vector

app = wx.App(False)
frame = wx.Frame(None, title="Starsplosion", size=(1280, 720))
panel = wx.Panel(frame)

world = World.World()

def SimulateAll(event=None):
	for object in world.all[:]:
	
		if object.destroyed or Vector.Magnitude(object.position) > 1500:
			world.RemoveObject(object)
			
		else:
			object.Simulate()
	
	panel.Refresh()

def PaintAll(event):
	dc = wx.PaintDC(event.GetEventObject())
	dc.Clear()
	
	for object in world.all:
		object.Draw(dc)
		
	HUD.Draw(dc)
		
world.AddObject(Ship.Ship( 0, [1280/4, 720/2], world ))
world.AddObject(Ship.Ship( 1, [1280*(3.0/4), 720/2], world ))

panel.Bind(wx.EVT_PAINT, PaintAll)
		
timer = wx.Timer(None)
timer.Bind(wx.EVT_TIMER, SimulateAll)
timer.Start(50)
		
frame.Show(True)
app.MainLoop()
