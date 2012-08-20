import pyglet
import os
import math

from Vector import *

worldPosition = (200, 200)
worldScale = 0.1

additiveSprites = ["exhaust", "explosion", "plasma", "deflector-field"]

batch = pyglet.graphics.Batch()

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
for f in os.listdir("./graphics/"):
   if f.endswith(".png"):
      name = f.split(".")[0].lower()

      image = pyglet.image.load("graphics/" + f)
      image.anchor_x, image.anchor_y = (image.width/2, image.height/2)
      
      images[name] = image
      availableSprites[name] = []
      usedSprites[name] = []


def freeAll():
   for name in usedSprites:
      availableSprites[name] = usedSprites[name]
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

def draw(name, position, rotation=0.0, scale=1.0, alpha=1.0):
   sprite = find(name)
   
   x, y = vectorScale(vectorAdd(position, worldPosition), worldScale)
   sprite.set_position(x, y)
      
   sprite.rotation = -180 * (rotation / math.pi)

   if scale * worldScale != sprite.scale:
      sprite.scale = scale * worldScale
      
   if int(alpha * 255.0) != sprite.opacity:
      sprite.opacity = int(alpha * 255.0)

def drawBatch():
   batch.draw()