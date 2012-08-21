from Vector import *
import Scalar
import math
import Ship
import Sprite

def drawEngine(engine):
   rotation = engine.parent.rotation + vectorDirection(engine.thrustVector) - math.pi
   
   Sprite.draw("engine-structure", engine.absolutePosition(), rotation + math.pi)
   Sprite.draw("engine", engine.absolutePosition(), rotation + math.pi)
   
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
   Sprite.draw("structure", cannon.absolutePosition(), cannon.parent.rotation)
   Sprite.draw("plasma-cannon", cannon.absolutePosition(), cannon.parent.rotation)

def drawDeflector(deflector):
   Sprite.draw("structure", deflector.absolutePosition(), deflector.parent.rotation)
   Sprite.draw("deflector", deflector.absolutePosition(), deflector.parent.rotation)

   alpha = deflector.parent.availableDeflectorPower / deflector.parent.maxDeflectorPower
   Sprite.draw("deflector-field", deflector.absolutePosition(), alpha=alpha, scale=2.5)      

def drawComputer(computer):
   Sprite.draw("structure", computer.absolutePosition(), computer.parent.rotation)
   Sprite.draw("computer", computer.absolutePosition(), computer.parent.rotation)

def drawStructure(structure):
   Sprite.draw("structure", structure.absolutePosition(), structure.parent.rotation)

moduleTypes = {}
moduleTypes["Engine"] = drawEngine
moduleTypes["PlasmaCannon"] = drawPlasmaCannon
moduleTypes["Deflector"] = drawDeflector
moduleTypes["FlightComputer"] = drawComputer
moduleTypes["Structure"] = drawStructure

def drawShip(ship):
   for m in ship.modules:

      type = m.__class__.__name__
      if type in moduleTypes:
         moduleTypes[type](m)
