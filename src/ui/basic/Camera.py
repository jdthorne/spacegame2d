from Vector import *
import Event
import App
import SmoothedValue

class Camera:
   def __init__(self, scale=1):
      self.onChange = Event.Event(self)

      self.scale = SmoothedValue.Scalar(scale)
      self.scale.onChange += self.handleValueUpdated

      self.position = SmoothedValue.Vector((0, 0))
      self.position.onChange += self.handleValueUpdated

   def handleValueUpdated(self, sender, value):
      self.onChange()

class WorldCamera(Camera):
   def __init__(self):
      Camera.__init__(self, 0.05)

      App.world.onUpdate += self.handleWorldUpdate

   def handleWorldUpdate(self, world):
      minPosition = (+99999, +99999)
      maxPosition = (-99999, -99999)

      for o in world.all:
         if o.exciting:
            minPosition = vectorElementMin(minPosition, o.position)
            maxPosition = vectorElementMax(maxPosition, o.position)
            
      mixSpeed = 0.05

      # Calculate scale based on max/min
      worldSize = vectorOffset(maxPosition, minPosition)
      if vectorMagnitude(worldSize) > 25:
         viewScale = vectorScale(vectorInvert(worldSize), 600)
         scale = min(viewScale)

         self.scale.set(scale)

      else:
         self.scale.set(0.05)

      # Calculate position based on center
      center = vectorAdd(minPosition, vectorScale(worldSize, 0.5))
      self.position.set(vectorScale(center, -1))

