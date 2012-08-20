#!/usr/bin/python

import time
import Timing
import Simulation

world = "time.time()"
fleets = ["james-battlestar", "james-swarm"]

simulation = Simulation.Simulation(fleets, world)

"""
import SimulationDisplay
import UserInterface
simulationDisplay = SimulationDisplay.SimulationDisplay(simulation)

ui = UserInterface.UserInterface()
ui.display(simulationDisplay)
ui.start()

"""

start = time.time()
printTime = start
frames = 0
sf = 0

print "Simulating..."
while (not simulation.complete()):
   simulation.tick()
   frames += 1
   sf += 1

   delta = time.time() - printTime
   if delta > 1.0:
      objects = len(simulation.world.all)
      fps = sf / delta
      print " => Running simulation @ %5.2ffps - completed %d frames, have %d objects" % (fps, frames, objects)

      printTime = time.time()
      sf = 0

print "Simulation complete - took %f seconds" % (time.time() - start,)



Timing.printAll()
