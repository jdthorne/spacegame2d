from Vector import *
import Scalar
import math
import Sprite

def drawBullet(bullet):
   if bullet.life > 2:
      Sprite.draw("plasma", bullet.position, scale=3.0, alpha=((1.0*bullet.life)/bullet.initialLife))

def drawExplosion(explosion):
   scale = explosion.life / 22.0
   alpha = float(explosion.life) / explosion.initialLife
   
   Sprite.draw("explosion", explosion.position, scale=scale, alpha=alpha)

