import MiscRender
import ShipRender

objectTypes = {}
objectTypes["Bullet"] = MiscRender.drawBullet
objectTypes["Explosion"] = MiscRender.drawExplosion
objectTypes["Ship"] = ShipRender.drawShip

def render(object):
   objectTypes[object.__class__.__name__](object)
