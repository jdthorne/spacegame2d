import pyglet
import os
import math

from Vector import *

worldPosition = (200, 200)
worldScale = 0.1

additiveSprites = ["exhaust", "explosion", "plasma", "deflector-field"]

batch = pyglet.graphics.Batch()
textBatch = pyglet.graphics.Batch()

backgroundLayer = pyglet.graphics.OrderedGroup(0)
structureLayer = pyglet.graphics.OrderedGroup(2)
moduleLayer = pyglet.graphics.OrderedGroup(3)
effectLayer = pyglet.graphics.OrderedGroup(4)
sidebarLayer = pyglet.graphics.OrderedGroup(5)
sidebarShipLayer = pyglet.graphics.OrderedGroup(6)
sidebarTextLayer = pyglet.graphics.OrderedGroup(7)
sidebarTextLayer2 = pyglet.graphics.OrderedGroup(8)

imageLayers = { "computer": moduleLayer,
                "deflector-field": effectLayer,
                "deflector": moduleLayer,
                "engine": moduleLayer,
                "exhaust": effectLayer,
                "explosion": effectLayer,
                "plasma-cannon": moduleLayer,
                "plasma": effectLayer,
                "structure-0": structureLayer,
                "structure-1": structureLayer,
                "structure-2": structureLayer,
                "engine-structure": moduleLayer,
                "sidebar": sidebarLayer,
                "ship-display": sidebarShipLayer,
                "team-display-0": sidebarShipLayer,
                "team-display-1": sidebarShipLayer,
                "team-display-2": sidebarShipLayer,
                "ship-deflector": sidebarTextLayer,
                "ship-ok": sidebarTextLayer2,
                "ship-damage": sidebarTextLayer2,
                "background": backgroundLayer,
                "ftl": moduleLayer,
                "vector-red": sidebarLayer,
                "vector-green": sidebarLayer,
                "vector-blue": sidebarLayer,
           }

images = {}

availableSprites = {}
usedSprites = {}
for f in os.listdir("./graphics/"):
   if f.endswith(".png") or f.endswith(".jpg"):
      name = f.split(".")[0].lower()

      image = pyglet.image.load("graphics/" + f)
      image.anchor_x, image.anchor_y = (image.width/2, image.height/2)

      if name.startswith("vector"):
         image.anchor_x = 0
      
      images[name] = image
      availableSprites[name] = []
      usedSprites[name] = []


def create(name):
   blend_src, blend_dest = (pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
   if name in additiveSprites:
      blend_src, blend_dest = (pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE)
   
   group = imageLayers[name]
      
   return pyglet.sprite.Sprite(images[name], group=group, 
                                             blend_src=blend_src, 
                                             blend_dest=blend_dest, 
                                             batch=batch)

def find(name):
   if len(availableSprites[name]) > 0:
      sprite = availableSprites[name][0]

      usedSprites[name].append(sprite)
      del availableSprites[name][0]

      return sprite

   else:
      sprite = create(name)
      usedSprites[name].append(sprite)
      
      return sprite

@Timing.timedFunction
def draw(name, position, rotation=0.0, scale=1.0, alpha=1.0, hud=False):
   if type(name) is str:
      sprite = find(name)
   else:
      sprite = name

   if hud:
      x, y = position 
   else:
      x, y = vectorScale(vectorAdd(position, worldPosition), worldScale)
      scale *= worldScale

   sprite.set_position(x, y)
      
   sprite.rotation = -180 * (rotation / math.pi)

   if scale != sprite.scale:
      sprite.scale = scale
      
   if int(alpha * 255.0) != sprite.opacity:
      sprite.opacity = int(alpha * 255.0)

labels = []
labelId = 0

def findLabel():
   global labelId 

   labelId += 1
   if labelId < len(labels):
      return labels[labelId]

   else:
      label = pyglet.text.Label("", anchor_x='left', anchor_y='center', 
                                    font_size=10, batch=textBatch,
                                    font_name="Helvetica")

      labels.append(label)
      return label

@Timing.timedFunction
def drawText(text, position, color=(255,255,255,255), bold=False, align="left"):
   label = findLabel()

   if label.text != text:
      label.text = text 

   if label.bold != bold:
      label.bold = bold

   x, y = position

   if label.x != x:
      label.x = x
   if label.y != y:
      label.y = y
   if label.color != color:
      label.color = color
   if label.anchor_x != align:
      label.anchor_x = align

@Timing.timedFunction
def freeAll():
   global labelId

   for name in usedSprites:
      availableSprites[name] = usedSprites[name]
      usedSprites[name] = []

   labelId = -1

@Timing.timedFunction
def drawBatch():
   if labelId < len(labels) - 1:
      for i in range(labelId+1, len(labels)):
         labels[i].x = -5000

   batch.draw()
   textBatch.draw()
