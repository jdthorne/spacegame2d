#!/usr/bin/python

import OpenGLCore
import HUD
import Ship
import World
import Vector
import Timing

world = World.World()
world.addObject(Ship.Ship( 0, (1280*0.5, 720.0*1.5), world ))
world.addObject(Ship.Ship( 0, (1280*1.0, 720.0*1.0), world ))
world.addObject(Ship.Ship( 0, (1280*1.5, 720.0*0.5), world ))
world.addObject(Ship.Ship( 0, (1280*2.0, 720.0*1.0), world ))
#world.addObject(Ship.Ship( 0, (1280*1.5, 720.0*0.25), world ))

world.addObject(Ship.Ship( 1, (1280*1.5, 720.0*2.0), world ))


OpenGLCore.runApplication(world)

Timing.printAll()
