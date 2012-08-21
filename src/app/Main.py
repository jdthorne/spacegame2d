#!/usr/bin/python

import sys
import time
import Timing
import Simulation

world = "time.time()"
fleets = ["james-battlestar", "james-swarm"]

simulation = Simulation.Simulation(fleets, world)

ui = ("--ui" in sys.argv)
if ui:
   import SimulationDisplay
   import UserInterface
   simulationDisplay = SimulationDisplay.SimulationDisplay(simulation)

   ui = UserInterface.UserInterface()
   ui.display(simulationDisplay)
   ui.start()

else:
   start = time.time()
   printTime = start
   frames = 0
   sf = 0
   minFps = 99999.0

   pot = 0
   potStart = time.time()

   print "Simulating..."
   while (not simulation.complete()):
      simulation.tick()
      frames += 1
      sf += 1

      delta = time.time() - printTime
      if delta > 0.2:
         objects = len(simulation.world.all)
         fps = sf / delta

         pot += 1
         if pot > 5:
            print " => Running simulation @ %5.2ffps - completed %d frames, have %d objects" % (fps, frames, objects)


         if fps < minFps:
            minFps = fps

         printTime = time.time()
         sf = 0

   totalTime = (time.time() - start)
   print
   print
   print "Simulation complete - averaged %.3ffps, min was %.3ffps" % (frames/totalTime, minFps)



Timing.printAll()
