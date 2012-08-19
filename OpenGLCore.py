
import os
import math
import pyglet

import Ship
import Scalar
import Vector
import Timing

additiveSprites = ["exhaust", "explosion", "plasma", "deflector-field"]
#additiveSprites = ["plasma"]

structureLayer = pyglet.graphics.OrderedGroup(0)
moduleLayer = pyglet.graphics.OrderedGroup(1)
effectLayer = pyglet.graphics.OrderedGroup(2)

imageLayers = { "computer": moduleLayer,
             "deflector-field": effectLayer,
            "deflector": moduleLayer,
            "engine": moduleLayer,
            "exhaust": effectLayer,
            "explosion": effectLayer,
            "plasma-cannon": moduleLayer,
            "plasma": effectLayer,
            "structure": structureLayer,
            "engine-structure": structureLayer,
           }

images = {}

availableSprites = {}
usedSprites = {}
for f in os.listdir("."):
   if f.endswith(".png"):
      name = f.split(".")[0].lower()

      image = pyglet.image.load(f)
      image.anchor_x, image.anchor_y = (image.width/2, image.height/2)
      
      images[name] = image
      availableSprites[name] = []
      usedSprites[name] = []

windowSize = (1680, 1050)
worldPosition = (200, 200)
worldScale = 1.0

halfWindowSize = Vector.scale(windowSize, 0.5)

batch = pyglet.graphics.Batch()

def orientWorld(world):
   global worldPosition
   global worldScale
   
   xMin, yMin = (9999999, 9999999)
   xMax, yMax = (-9999999, -9999999)
   for o in world.all[:]:
   	if o.exciting:
			x, y = o.position
			if x < xMin:
				xMin = x
			if x > xMax:
				xMax = x
				
			if y < yMin:
				yMin = y
			if y > yMax:
				yMax = y
         
   padding = 200
   xMin -= padding
   yMin -= padding
   xMax += padding
   yMax += padding
   
   xScale = 1280 / (xMax - xMin)
   yScale = 720 / (yMax - yMin)
   worldScale = (0.95 * worldScale) + (0.05 * min(2.0, xScale, yScale))
   
   minPos = (xMin, yMin)
   maxPos = (xMax, yMax)
   center = Vector.scale(Vector.add(minPos, maxPos), -0.5)

   worldPosition = Vector.add(Vector.scale(worldPosition, 0.95), Vector.scale(center, 0.05))
      

@Timing.timedFunction("Draw/Free")
def freeAllSprites():
   for name in usedSprites:
      availableSprites[name] = usedSprites[name]
      usedSprites[name] = []

@Timing.timedFunction("Draw/Sprite/Create")
def createSprite(name):
   blend_src, blend_dest = (pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
   if name in additiveSprites:
      blend_src, blend_dest = (pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE)
   
   group = imageLayers[name]
      
   return pyglet.sprite.Sprite(images[name], group=group, blend_src=blend_src, blend_dest=blend_dest, batch=batch)

@Timing.timedFunction("Draw/Sprite/Find")
def findSprite(name):
   if len(availableSprites[name]) > 0:
      sprite = availableSprites[name][0]

      usedSprites[name].append(sprite)
      del availableSprites[name][0]

      return sprite

   else:
      sprite = createSprite(name)
      usedSprites[name].append(sprite)
      
      return sprite

@Timing.timedFunction("Draw/Sprite")
def drawSprite(name, position, rotation=0.0, scale=1.0, alpha=1.0):
   sprite = findSprite(name)
   
   x, y = Vector.add(Vector.scale(Vector.add(position, worldPosition), worldScale), halfWindowSize)
   sprite.set_position(x, y)
      
   sprite.rotation = -180 * (rotation / math.pi)

   if scale * worldScale != sprite.scale:
      sprite.scale = scale * worldScale
      
   if int(alpha * 255.0) != sprite.opacity:
      sprite.opacity = int(alpha * 255.0)

# =================== FUNCTIONS FOR DRAWING VARIOUS OBJECTS =================

def drawBullet(bullet):
   if bullet.life > 2:
      drawSprite("plasma", bullet.position, scale=3.0, alpha=((1.0*bullet.life)/bullet.initialLife))

def drawExplosion(explosion):
   scale = explosion.life / 22.0
   alpha = float(explosion.life) / explosion.initialLife
   
   drawSprite("explosion", explosion.position, scale=scale, alpha=alpha)
   
@Timing.timedFunction("Draw/Ship/Engine")
def drawEngine(engine):
   rotation = engine.parent.rotation + Vector.direction(engine.thrustVector) - math.pi
   
   drawSprite("engine-structure", engine.absolutePosition(), rotation + math.pi)
   drawSprite("engine", engine.absolutePosition(), rotation + math.pi)
   
   if engine.power > 0.01:
      engine.onTime += 1
   else:
      engine.onTime -= 2

   engine.onTime = Scalar.bound(0, engine.onTime, 20)

   onPower = engine.onTime / 20.0
   if onPower > 0.05:
      exhaustDirection = Vector.rotate(Vector.scale(engine.thrustVector, -1), engine.parent.rotation)
      exhaustPoint = Vector.scale(Vector.normalize(exhaustDirection), Ship.MODULE_SIZE)
      exhaustPoint = Vector.add(engine.absolutePosition(), exhaustPoint)
   
      rotation = engine.parent.rotation + Vector.direction(engine.thrustVector) + (math.pi/2)
      drawSprite("exhaust", exhaustPoint, rotation, alpha=onPower)

def drawPlasmaCannon(cannon):
   drawSprite("structure", cannon.absolutePosition(), cannon.parent.rotation)
   drawSprite("plasma-cannon", cannon.absolutePosition(), cannon.parent.rotation)

def drawDeflector(deflector):
   drawSprite("structure", deflector.absolutePosition(), deflector.parent.rotation)
   drawSprite("deflector", deflector.absolutePosition(), deflector.parent.rotation)

   alpha = deflector.availablePower
   drawSprite("deflector-field", deflector.absolutePosition(), alpha=alpha, scale=2.5)      

def drawComputer(computer):
   drawSprite("structure", computer.absolutePosition(), computer.parent.rotation)
   drawSprite("computer", computer.absolutePosition(), computer.parent.rotation)

def drawStructure(structure):
   drawSprite("structure", structure.absolutePosition(), structure.parent.rotation)

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

objectTypes = {}
objectTypes["Bullet"] = drawBullet
objectTypes["Explosion"] = drawExplosion
objectTypes["Ship"] = drawShip

# =================== CORE LOOP =================
def renderObject(obj):
   name = obj.__class__.__name__
   
   #w, h = Vector.scale((1280, 720), 1.0/worldScale)
   #x, y = obj.position
   #if x < 0 or x > w:
   #   return
   #if y < 0 or y > h:
   #   return
   
   if name in objectTypes:
      objectTypes[name](obj)
   
def runApplication(world):
   pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
   pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
   window = pyglet.window.Window(width=windowSize[0], height=windowSize[1])
   fpsDisplay = pyglet.clock.ClockDisplay()

   @Timing.timedFunction("Simulate")
   def tick(dt):
      world.simulate()
      
      if not world.hasRemainingExcitement():
         pyglet.app.exit()
      
   @Timing.timedFunction("Draw")
   def drawAll():
      orientWorld(world)
      freeAllSprites()
      for item in world.all[:]:
         renderObject(item)
      
      drawBatch()
         
   @Timing.timedFunction("Draw/Batch")
   def drawBatch():
      batch.draw()
      
   @window.event
   def on_draw():
      window.clear()
      drawAll()
      fpsDisplay.draw()
   
   pyglet.clock.set_fps_limit(60.0)
   pyglet.clock.schedule_interval(tick, 1/30.0)
   
   pyglet.app.run()


