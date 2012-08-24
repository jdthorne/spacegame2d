
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
class Drawable:
   def __init__(self, camera, position, rotation, scale):
      self.camera = camera
      self.camera.onChange += self.handleCameraChanged

      self.setPosition(position)
      self.setRotation(rotation)
      self.setScale(scale)

   def setPosition(self, position):
      self.position = position

      position = vectorAdd(position, self.camera.position())
      position = vectorScale(position, self.camera.scale())
      
      position = vectorAdd(position, App.ui.windowCenter)

      self.drawable.x, self.drawable.y = position

   def setRotation(self, rotation):
      rotation = -180 * (rotation / math.pi)
      self.drawable.rotation = rotation

   def setScale(self, scale):
      self.scale = scale 

      scale *= self.camera.scale()
      self.drawable.scale = scale

   def setAlpha(self, alpha):
      self.drawable.opacity = scalarBound(0, int(255.0 * alpha), 255)

   def handleCameraChanged(self, camera):
      self.setPosition(self.position)
      self.setScale(self.scale)

   def destroy(self):
      self.camera.onChange -= self.handleCameraChanged

      self.drawable.delete()
      self.drawable = None   

class Sprite(Drawable):
   def __init__(self, image, camera=App.hudCamera, position=(99999, 99999), rotation=0, scale=1.0, additive=False):
      if type(image) is str:
         image = images[image]

      blend_src, blend_dest = (pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
      if additive:
         blend_src, blend_dest = (pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE)
   
      self.drawable = pyglet.sprite.Sprite(image, batch=App.ui.batch, 
                                                  blend_src=blend_src, 
                                                  blend_dest=blend_dest)

      Drawable.__init__(self, camera, position, rotation, scale)




class Text(Drawable):
   def __init__(self, text, camera=App.hudCamera, position=(99999, 99999), rotation=0, scale=1.0, bold=False, align="left"):
      self.drawable = pyglet.text.Label(text, batch=App.ui.batchText, 
                                              bold=bold, 
                                              anchor_x=align, 
                                              color=(0, 0, 0, 255), 
                                              font_size=10,
                                              font_name="Helvetica")

      Drawable.__init__(self, camera, position, rotation, scale)

   def setText(self, text):
      if self.drawable.text != text:
         self.drawable.text = text