import Render
import Sprite
from Vector import *
import UserInterface

# This class displays a simulation on the User Interface
class SimulationDisplay:
   def __init__(self, simulation):
      self.simulation = simulation

   def draw(self):
      self.orientWorld()
      for item in self.simulation.world.all[:]:
         Render.render(item)

   def complete(self):
      return self.simulation.complete()

   def tick(self):
      self.simulation.tick()

   def orientWorld(self):
      world = self.simulation.world 

      xMin, yMin = (9999999, 9999999)
      xMax, yMax = (-9999999, -9999999)
      for o in world.all[:]:
         if o.exciting:
            x, y = o.position
            if x < xMin:
               xMin = x
            if x > xMax:
               xMax = x
               
            if y < yMin:
               yMin = y
            if y > yMax:
               yMax = y
            
      padding = 200
      xMin -= padding
      yMin -= padding
      xMax += padding
      yMax += padding
      
      xScale = 1280 / (xMax - xMin)
      yScale = 720 / (yMax - yMin)
      Sprite.worldScale = (0.95 * Sprite.worldScale) + (0.05 * min(2.0, xScale, yScale))

      if Sprite.worldScale > 1.5:
         Sprite.worldScale = 1.5
      
      minPos = (xMin, yMin)
      maxPos = (xMax, yMax)
      center = vectorScale(vectorAdd(minPos, maxPos), -0.5)

      center = vectorAdd(center, vectorScale(UserInterface.halfWindowSize, 1.0/Sprite.worldScale))

      Sprite.worldPosition = vectorAdd(vectorScale(Sprite.worldPosition, 0.95), vectorScale(center, 0.05))

