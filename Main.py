#!/usr/bin/python

import OpenGLCore
import HUD
import Ship
import World
import Vector
import Timing
import time

seed = time.time()
print " => Seed is ", seed

world = World.World(seed=seed)
worldSize = 4500
def randomPosition():
   while True:
      newPosition = (world.randomValue(-worldSize, worldSize), world.randomValue(-worldSize, worldSize))
      
      minDistance = 999999999
      for obj in world.all:
         distance = Vector.magnitude(Vector.offset( obj.position, newPosition))
         
         if distance < minDistance:
            minDistance = distance
      
      if minDistance > 500:
         return newPosition


world.addObject(Ship.Ship( 1, randomPosition(), world ))

for i in range(15):
   world.addObject(Ship.Ship( 0, randomPosition(), world ))


OpenGLCore.runApplication(world)

Timing.printAll()
