import App
import MiscRender
import ShipRender

createObjectRenderer = {
   "Bullet": MiscRender.BulletRenderer,
   "Explosion": MiscRender.ExplosionRenderer,
   "Ship": ShipRender.ShipRenderer
}

class WorldRenderer:
   def __init__(self):
      App.world.onObjectAdded += self.handleObjectAdded

      self.objectRenderers = []

   def handleObjectAdded(self, world, object):
      type = object.__class__.__name__
      renderer = createObjectRenderer[type](object)

      self.objectRenderers.append(renderer)