from Vector import *
from Scalar import *
import Event
import App
import SmoothedValue

class Camera:
   def __init__(self, scale=1):
      self.onChange = Event.Event(self)

      self.scale = SmoothedValue.Scalar(scale, self.handleValueUpdated)
      self.position = SmoothedValue.Vector((0, 0), self.handleValueUpdated)

   def handleValueUpdated(self, sender, value):
      self.onChange()

   def toWorldCoordinates(self, screenCoordinates):
      position = screenCoordinates

      #position = vectorSub(position, App.ui.windowCenter)

      position = vectorScale(position, 1.0 / self.scale())
      position = vectorSub(position, self.position())

      return position

   def toScreenCoordinates(self, worldCoordinates):
      position = worldCoordinates

      position = vectorAdd(position, self.position())
      position = vectorScale(position, self.scale())
      
      position = vectorAdd(position, App.ui.windowCenter)

      return position

class WorldCamera(Camera):
   def __init__(self):
      Camera.__init__(self, 0.05)

      self.focus = None
      App.world.onUpdate += self.handleWorldUpdate

   def handleWorldUpdate(self, world):
      if self.focus != None:
         self.position.set(vectorScale(self.focus.position, -1))
         self.scale.set(1.0)

      else:
         minPosition, maxPosition = vectorBounds([o.position for o in world.all if o.exciting])

         # Calculate scale based on max/min
         worldSize = vectorOffset(maxPosition, minPosition)
         viewScale = vectorScale(vectorInvert(worldSize), 600)
         scale = min(viewScale)

         self.scale.set(scale)

         # Calculate position based on center
         center = vectorAdd(minPosition, vectorScale(worldSize, 0.5))
         self.position.set(vectorScale(center, -1))

