#!/usr/bin/python

import OpenGLCore
import HUD
import Ship
import World
import Vector
import Timing

world = World.World()
worldSize = 3000
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

world.addObject(Ship.Ship( 0, randomPosition(), world ))
world.addObject(Ship.Ship( 0, randomPosition(), world ))
world.addObject(Ship.Ship( 0, randomPosition(), world ))
world.addObject(Ship.Ship( 0, randomPosition(), world ))
world.addObject(Ship.Ship( 0, randomPosition(), world ))

world.addObject(Ship.Ship( 1, randomPosition(), world ))


OpenGLCore.runApplication(world)

Timing.printAll()
