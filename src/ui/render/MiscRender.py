from Vector import *
from Scalar import *
import math
import Sprite
import App
import Event

class SimpleRenderer:
   def __init__(self, object, image):
      object.onUpdate += self.handleUpdate
      object.onDestroy += self.handleDestroy

      self.sprite = Sprite.create(image, camera=App.worldCamera, additive=True)

   def handleUpdate(self, object):
      self.sprite.setPosition(object.position)
      self.updateEffects(object)

   def handleDestroy(self, object):
      object.onUpdate -= self.handleUpdate
      object.onDestroy -= self.handleDestroy

      self.sprite.destroy()

class BulletRenderer(SimpleRenderer):
   def __init__(self, bullet):
      SimpleRenderer.__init__(self, bullet, "plasma")

   def updateEffects(self, bullet):
      self.sprite.setScale(4.0)
      self.sprite.setAlpha((1.0*bullet.life)/bullet.initialLife)

class ExplosionRenderer(SimpleRenderer):
   def __init__(self, bullet):
      SimpleRenderer.__init__(self, bullet, "explosion")

   def updateEffects(self, explosion):
      self.sprite.setScale((explosion.life**1.1) / 25.0)
      self.sprite.setAlpha(float(explosion.life) / explosion.initialLife)
