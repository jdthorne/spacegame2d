
import os
import math
import pyglet
import App

from Scalar import *
from Vector import *

# ================= LOAD IMAGES =========================
images = {}
for f in os.listdir("./graphics/"):
   if f.endswith(".png") or f.endswith(".jpg"):
      name = f.split(".")[0].lower()

      image = pyglet.image.load("graphics/" + f)
      image.anchor_x, image.anchor_y = (image.width/2, image.height/2)

      if name.startswith("vector"):
         image.anchor_x = 0
      
      images[name] = image

# ================ THE SPRITE WRAPPER CLASS ==============
class Sprite:
   def __init__(self, image, camera, position=(0, 0), rotation=0, scale=1.0, additive=False):
      if type(image) is str:
         image = images[image]

      self.camera = camera
      self.camera.onChange += self.handleCameraChanged

      blend_src, blend_dest = (pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
      if additive:
         blend_src, blend_dest = (pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE)
   
      self.sprite = pyglet.sprite.Sprite(image, batch=App.ui.batch, 
                                                blend_src=blend_src, 
                                                blend_dest=blend_dest)

      self.setPosition(position)
      self.setRotation(rotation)
      self.setScale(scale)

   def setPosition(self, position):
      self.position = position

      position = vectorAdd(position, self.camera.position())
      position = vectorScale(position, self.camera.scale())
      
      position = vectorAdd(position, App.ui.windowCenter)

      self.sprite.set_position(position[0], position[1])

   def setRotation(self, rotation):
      rotation = -180 * (rotation / math.pi)
      self.sprite.rotation = rotation

   def setScale(self, scale):
      self.scale = scale 

      scale *= self.camera.scale()
      self.sprite.scale = scale

   def setAlpha(self, alpha):
      self.sprite.opacity = scalarBound(0, int(255.0 * alpha), 255)

   def handleCameraChanged(self, camera):
      self.setPosition(self.position)
      self.setScale(self.scale)

   def destroy(self):
      self.camera.onChange -= self.handleCameraChanged

      self.sprite.delete()
      self.sprite = None

# ================ THINGS THAT ARE USEFUL ================
def create(image, camera=App.hudCamera, position=(0, 0), rotation=0, scale=1.0, additive=False):
   return Sprite(image, camera, position, rotation, scale, additive)
