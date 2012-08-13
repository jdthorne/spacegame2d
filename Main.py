#!/opt/local/bin/python

import Ship
import wx

app = wx.App(False)
frame = wx.Frame(None, title="Starsplosion", size=(1280, 720))
panel = wx.Panel(frame)

all = [ Ship.Ship() ]

def SimulateAll(event=None):
	for object in all:
		object.Simulate()
	
	panel.Refresh()

def PaintAll(event):
	dc = wx.PaintDC(event.GetEventObject())
	dc.Clear()
	
	for object in all:
		object.Draw(dc)

panel.Bind(wx.EVT_PAINT, PaintAll)
		
timer = wx.Timer(None)
timer.Bind(wx.EVT_TIMER, SimulateAll)
timer.Start(50)
		
frame.Show(True)
app.MainLoop()
