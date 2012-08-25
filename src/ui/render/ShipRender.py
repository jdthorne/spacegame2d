from Vector import *
from pyglet.gl import *
from Scalar import *
import math
import Ship
import Sprite
import pyglet
import Misc
import App
import MiscRender

class ShipRenderer:
   def __init__(self, ship):
      self.ship = ship

      ship.onUpdate += self.handleUpdate
      ship.onDestroy += self.handleDestroy
      ship.onLayoutChanged += self.handleLayoutChanged

      self.wasDestroyed = False
      self.sprite = None

      self.deflectorSprite = Sprite.Sprite("deflector-field", camera=App.worldCamera, scale=4)
      self.ftlSprite = Sprite.Sprite("ftl", camera=App.worldCamera, scale=10)

      self.generateSprite()

   def handleUpdate(self, ship):
      self.sprite.setPosition(ship.position)
      self.sprite.setRotation(ship.rotation)

      if ship.combatTeam != None:
         self.deflectorSprite.setAlpha(ship.availableDeflectorPower / ship.maxDeflectorPower)
         self.deflectorSprite.setPosition(ship.position)

      if ship.ftlTime > 0:
         self.ftlSprite.setAlpha(ship.ftlTime / 25.0)
         self.ftlSprite.setPosition(ship.position)
      elif self.ftlSprite != None:
         self.ftlSprite.destroy()
         self.ftlSprite = None

   def handleDestroy(self, ship):
      ship.onUpdate -= self.handleUpdate
      ship.onDestroy -= self.handleDestroy

      self.sprite.destroy()
      self.deflectorSprite.destroy()

      if self.ftlSprite != None:
         self.ftlSprite.destroy()
         self.ftlSprite = None

      self.wasDestroyed = True

   def handleLayoutChanged(self, ship):
      if not self.wasDestroyed:
         self.generateSprite()

   def generateSprite(self):
      if self.sprite != None:
         self.sprite.destroy()

      size = (768, 768)

      isWeapon = lambda module: module.__class__.__name__ == "PlasmaCannon"
      isComputer = lambda module: module.__class__.__name__ == "FlightComputer"
      isEngine = lambda module: module.__class__.__name__ == "Engine"
      isDeflector = lambda module: module.__class__.__name__ == "Deflector"

      image = pyglet.image.Texture.create(size[0], size[1])
      offset = vectorScale(size, 0.5)

      imagetex = image.get_texture()
      texfrmbuf =(GLuint*1)()
      glEnable(GL_BLEND)
      glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
      glGenFramebuffersEXT(1, texfrmbuf)
      glBindFramebufferEXT(GL_DRAW_FRAMEBUFFER_EXT, texfrmbuf[0])
      glFramebufferTexture2DEXT(GL_DRAW_FRAMEBUFFER_EXT, GL_COLOR_ATTACHMENT0_EXT, imagetex.target, image.id, 0)


      structureImage = "structure-0"
      if self.ship.combatTeam != None:
         structureImage = "structure-%d" % (self.ship.combatTeam.id,)

      for module in self.ship.modules:
         if (not isEngine(module)):
            x, y = vectorAdd(module.position, offset)
            x, y = (int(x), int(y))

            Sprite.images[structureImage].blit(x, y)

      for module in self.ship.modules:
         x, y = vectorAdd(module.position, offset)
         x, y = (int(x), int(y))

         if isEngine(module):
            engine = module

            if engine.thrustVector[0] > 0:
               Sprite.images["engine-structure"].blit(x, y)
            else:
               Sprite.images["engine-structure@180"].blit(x, y)

      for module in self.ship.modules:
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

      self.sprite = Sprite.Sprite(image, camera=App.worldCamera)
      self.handleUpdate(self.ship)

# ======================= STRUCTURAL/CACHING STUFF =========================

"""

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


EVEN OLDER


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