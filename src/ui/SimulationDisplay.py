import Render
import Sprite
import Scalar
import math
from Vector import *
import UserInterface

viewWindowCenter = vectorAdd(UserInterface.halfWindowSize, (-120,0))


# This class displays a simulation on the User Interface
class SimulationDisplay:
   def __init__(self, simulation):
      self.simulation = simulation
      self.zoomedShip = None

   def draw(self):
      Sprite.draw("background", position=UserInterface.halfWindowSize, hud=True)

      self.orientWorld()
      for item in self.simulation.world.all:
         Render.render(item)

      self.drawSidebar()

   def drawSidebar(self):
      sidebarX = UserInterface.windowSize[0] - 240/2
      sidebarY = UserInterface.windowSize[1]/2
      Sprite.draw("sidebar", position=(sidebarX, sidebarY), hud=True)

      self.shipY = UserInterface.windowSize[1] - 30

      for team in self.simulation.world.combatTeams:
         Sprite.draw("team-display-%d" % (team,), position=(sidebarX, self.shipY-3), hud=True)
         Sprite.drawText("Team %d" % (team,), position=(sidebarX, self.shipY - 5), bold=True, 
                                              align="center", color=(0,0,0,255))
         self.shipY -= 35

         for ship in self.simulation.world.combatTeams[team]:
            self.drawSidebarShip(ship)
            self.shipY -= 30

         self.shipY -= 25

   def drawSidebarShip(self, ship):
      sidebarX = UserInterface.windowSize[0] - 240/2

      Sprite.draw("ship-display", position=(sidebarX, self.shipY), hud=True)

      if not ship.destroyed:
         color = (0, 0, 0, 255)

         power = Scalar.bound(0, ship.availableDeflectorPower / ship.maxDeflectorPower, 1.0)
         delta = int(power * 30)
         if delta == 29:
            delta = 30

         statusAlpha, status = ship.status
         Sprite.draw("ship-deflector", position=(UserInterface.windowSize[0] - 10 + 15 - delta, self.shipY), hud=True)

         if not ship.hasTakenDamage:
            Sprite.draw("ship-ok", position=(UserInterface.windowSize[0] - 5, self.shipY), hud=True)
         else:
            Sprite.draw("ship-damage", position=(UserInterface.windowSize[0] - 5, self.shipY), hud=True)

         statusColor = (0, 0, 0, int(Scalar.bound(0.2,statusAlpha,1.0)*255))

         Sprite.drawText(ship.name, position=(sidebarX - 110, self.shipY), bold=True, color=color)
         Sprite.drawText(status.lower(), position=(sidebarX - 20, self.shipY), bold=False, color=statusColor)

   def complete(self):
      return self.simulation.complete()

   def tick(self, dt):
      self.simulation.tick()

   def orientWorld(self):
      world = self.simulation.world 

      if self.zoomedShip == None:
         xMin, yMin = (9999999, 9999999)
         xMax, yMax = (-9999999, -9999999)
         for o in world.all:
            if o.exciting and not o.destroyed:
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
         
         xScale = (1280-240) / (xMax - xMin)
         yScale = 720 / (yMax - yMin)
         scale = min(1.0, xScale, yScale)
         
         minPos = (xMin, yMin)
         maxPos = (xMax, yMax)
         center = vectorScale(vectorAdd(minPos, maxPos), -0.5)

         mixSpeed = 0.05

      else:
         center = vectorScale(self.zoomedShip.position, -1)
         scale = 0.3
         mixSpeed = 0.2

      mixA = 1.0 - mixSpeed
      mixB = mixSpeed
      Sprite.worldScale = (mixA * Sprite.worldScale) + (mixB * scale)
      if Sprite.worldScale > 1.5:
         Sprite.worldScale = 1.5

      center = vectorAdd(center, vectorScale(viewWindowCenter, 1.0/Sprite.worldScale))
      Sprite.worldPosition = vectorAdd(vectorScale(Sprite.worldPosition, mixA), vectorScale(center, mixB))

   def handleMouseMotion(self, x, y, dx, dy):
      if x > UserInterface.windowSize[0] - 240:

         self.shipY = UserInterface.windowSize[1] - 30

         for team in self.simulation.world.combatTeams:
            self.shipY -= 35

            for ship in self.simulation.world.combatTeams[team]:
               if not ship.destroyed:
                  if y <= self.shipY + 15 and y > self.shipY - 15:
                     self.zoomedShip = ship
                     return

               self.shipY -= 30

            self.shipY -= 25

      self.zoomedShip = None
