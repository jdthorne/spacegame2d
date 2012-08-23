import MiscRender
import ShipRender

objectTypes = {}
objectTypes["Bullet"] = MiscRender.drawBullet
objectTypes["Explosion"] = MiscRender.drawExplosion
objectTypes["Ship"] = ShipRender.drawShip

def render(world):
   for object in world.all:
      objectTypes[object.__class__.__name__](object)

def clean():
   ShipRender.cleanAll()