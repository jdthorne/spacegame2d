from Vector import *
import Scalar
import math
import Ship
import Sprite

def drawEngine(engine):
   rotation = engine.parent.rotation + vectorDirection(engine.thrustVector) - math.pi
   
   Sprite.draw("engine-structure", engine.absolutePosition(), rotation + math.pi)
   #Sprite.draw("engine", engine.absolutePosition(), rotation + math.pi)
   
   if engine.power > 0.01:
      engine.onTime += 1
   else:
      engine.onTime -= 2

   engine.onTime = Scalar.bound(0, engine.onTime, 20)

   onPower = engine.onTime / 20.0
   if onPower > 0.05:
      exhaustDirection = vectorRotate(vectorScale(engine.thrustVector, -1), engine.parent.rotation)
      exhaustPoint = vectorScale(vectorNormalize(exhaustDirection), Ship.MODULE_SIZE)
      exhaustPoint = vectorAdd(engine.absolutePosition(), exhaustPoint)
   
      rotation = engine.parent.rotation + vectorDirection(engine.thrustVector) + (math.pi/2)
      Sprite.draw("exhaust", exhaustPoint, rotation, alpha=onPower)

def drawPlasmaCannon(cannon):
   Sprite.draw("plasma-cannon", cannon.absolutePosition(), cannon.parent.rotation)

def drawDeflector(deflector):
   Sprite.draw("deflector", deflector.absolutePosition(), deflector.parent.rotation)

def drawComputer(computer):
   Sprite.draw("computer", computer.absolutePosition(), computer.parent.rotation)

moduleTypes = {}
moduleTypes["Engine"] = drawEngine
#moduleTypes["PlasmaCannon"] = drawPlasmaCannon
#moduleTypes["Deflector"] = drawDeflector
moduleTypes["FlightComputer"] = drawComputer

def drawShip(ship):

   alpha = ship.availableDeflectorPower / ship.maxDeflectorPower
   Sprite.draw("deflector-field", ship.position, alpha=alpha, scale=3)      

   for m in ship.modules:

      type = m.__class__.__name__
      if type != "Engine":
         Sprite.draw("structure-%d" % (ship.combatTeam,), 
                     m.absolutePosition(), 
                     ship.rotation)

      if type in moduleTypes:
         moduleTypes[type](m)
