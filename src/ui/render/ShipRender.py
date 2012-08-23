from Vector import *
from pyglet.gl import *
from Scalar import *
import math
import Ship
import Sprite
import pyglet
import Misc

# ======================= STRUCTURAL/CACHING STUFF =========================

def isWeapon(module):
   return module.__class__.__name__ == "PlasmaCannon"
def isComputer(module):
   return module.__class__.__name__ == "FlightComputer"
def isEngine(module):
   return module.__class__.__name__ == "Engine"
def isDeflector(module):
   return module.__class__.__name__ == "Deflector"

def renderStructureToSprite(ship):
   size = (768, 768)

   image = pyglet.image.Texture.create(size[0], size[1])
   offset = vectorScale(size, 0.5)

   imagetex = image.get_texture()
   texfrmbuf =(GLuint*1)()
   glEnable(GL_BLEND)
   glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
   glGenFramebuffersEXT(1, texfrmbuf)
   glBindFramebufferEXT(GL_DRAW_FRAMEBUFFER_EXT, texfrmbuf[0])
   glFramebufferTexture2DEXT(GL_DRAW_FRAMEBUFFER_EXT, GL_COLOR_ATTACHMENT0_EXT, imagetex.target, image.id, 0)

   for module in ship.modules:
      if (not isEngine(module)):
         x, y = vectorAdd(module.position, offset)
         x, y = (int(x), int(y))

         Sprite.images["structure-%d" % (ship.combatTeam,)].blit(x, y)

   for module in ship.modules:
      x, y = vectorAdd(module.position, offset)
      x, y = (int(x), int(y))

      if isEngine(module):
         engine = module

         if engine.thrustVector[0] > 0:
            Sprite.images["engine-structure"].blit(x, y)
         else:
            Sprite.images["engine-structure@180"].blit(x, y)

   for module in ship.modules:
      x, y = vectorAdd(module.position, offset)
      x, y = (int(x), int(y))

      if isComputer(module):
         Sprite.images["computer"].blit(x, y)
      elif isWeapon(module):
         Sprite.images["plasma-cannon"].blit(x, y)
      elif isDeflector(module):
         Sprite.images["deflector"].blit(x, y)

   glFlush()
   glDisable(GL_BLEND)
   glDeleteFramebuffersEXT(1, texfrmbuf)
   glBindFramebufferEXT(GL_DRAW_FRAMEBUFFER_EXT, 0)

   image.anchor_x = offset[0]
   image.anchor_y = offset[1]
   return pyglet.sprite.Sprite(image, batch=Sprite.batch, group=Sprite.structureLayer)

# ======================= COMPLICATED EFFECTS ===============================
def drawEngineFlame(engine):
   rotation = engine.parent.rotation + vectorDirection(engine.thrustVector) - math.pi
   
   if engine.power > 0.01:
      engine.onTime += 1
   else:
      engine.onTime -= 2

   engine.onTime = scalarBound(0, engine.onTime, 20)

   onPower = engine.onTime / 20.0
   if onPower > 0.05:
      exhaustDirection = vectorRotate(vectorScale(engine.thrustVector, -1), engine.parent.rotation)
      exhaustPoint = vectorScale(vectorNormalize(exhaustDirection), Misc.MODULE_SIZE)
      exhaustPoint = vectorAdd(engine.absolutePosition(), exhaustPoint)
   
      rotation = engine.parent.rotation + vectorDirection(engine.thrustVector) + (math.pi/2)
      Sprite.draw("exhaust", exhaustPoint, rotation, alpha=onPower)


# ======================= TOP-LEVEL DRAWING STUFF ===========================
structures = {}
def clean(ship):
   if ship in structures:
      structure = structures[ship]
      del structures[ship]
      structure.delete()

def drawStructure(ship):
   if ship.destroyed:
      clean(ship)
      return

   if (ship.damaged) or (ship not in structures):
      clean(ship)
      structures[ship] = renderStructureToSprite(ship)

   Sprite.draw(structures[ship], ship.position, rotation=ship.rotation)

def drawEffects(ship):
   alpha = ship.availableDeflectorPower / ship.maxDeflectorPower
   Sprite.draw("deflector-field", ship.position, alpha=alpha, scale=4)      

   for engine in ship.engines:
      drawEngineFlame(engine)      

   if ship.ftlTime > 0:
      alpha = ship.ftlTime / 25.0
      Sprite.draw("ftl", ship.position, alpha=alpha, scale=10)


def drawShip(ship):
   drawStructure(ship)
   drawEffects(ship)

def cleanAll():
   ships = []
   for ship in structures.copy():
      clean(ship)


"""



def drawEngine(engine):

def drawPlasmaCannon(cannon):
   Sprite.draw("plasma-cannon", cannon.absolutePosition(), cannon.parent.rotation)

def drawDeflector(deflector):
   Sprite.draw("deflector", deflector.absolutePosition(), deflector.parent.rotation)

moduleTypes = {}
moduleTypes["Engine"] = drawEngine
#moduleTypes["PlasmaCannon"] = drawPlasmaCannon
#moduleTypes["Deflector"] = drawDeflector
#moduleTypes["FlightComputer"] = drawComputer

shipBodies = {}
def renderShipBody(ship):
   if (not ship.damaged) and (ship in shipBodies):
      return



def drawShip(ship):

   renderShipBody(ship)

   for m in ship.modules:
      type = m.__class__.__name__

      if type in moduleTypes:
         moduleTypes[type](m)
"""