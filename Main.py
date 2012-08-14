#!/opt/local/bin/python

import Ship
import wx

app = wx.App(False)
frame = wx.Frame(None, title="Starsplosion", size=(1280, 720))
panel = wx.Panel(frame)

all = []

def SimulateAll(event=None):
	for object in all:
		object.Simulate()
	
	panel.Refresh()

def PaintAll(event):
	dc = wx.PaintDC(event.GetEventObject())
	dc.Clear()
	
	for object in all:
		object.Draw(dc)
		
def Scan():
	return all
	
all.append(Ship.Ship( [1280/4, 720/2], scanner=Scan, powered=True ))
all.append(Ship.Ship( [1280*(3.0/4), 720/2] ))

panel.Bind(wx.EVT_PAINT, PaintAll)
		
timer = wx.Timer(None)
timer.Bind(wx.EVT_TIMER, SimulateAll)
timer.Start(50)
		
frame.Show(True)
app.MainLoop()
