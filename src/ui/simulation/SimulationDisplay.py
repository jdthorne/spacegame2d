import Render
import Sprite
from Scalar import *
import math
from Vector import *
import UserInterface
import Simulation
import HUD
import Misc

viewWindowCenter = vectorAdd(UserInterface.halfWindowSize, (-120,0))


# This class displays a simulation on the User Interface
class SimulationDisplay:
   def __init__(self, simulation):
      self.simulation = simulation
      self.zoomedShip = None

      self.leftEdge = -5000
      self.rightEdge = 5000
      self.topEdge = 5000
      self.bottomEdge = -5000

   def draw(self):
      self.orientWorld()
      for item in self.simulation.world.all:
         Render.render(item)

      HUD.draw(self.zoomedShip)
      self.drawSidebar()

   def drawSidebar(self):
      sidebarX = UserInterface.windowSize[0] - 240/2
      sidebarY = UserInterface.windowSize[1]/2

      self.shipY = UserInterface.windowSize[1] - 30

      for team in self.simulation.world.combatTeams:
         Sprite.draw("team-display-%d" % (team,), position=(sidebarX, self.shipY-3), hud=True)
         Sprite.drawText("Battle Fleet %d" % (team,), position=(sidebarX, self.shipY - 5), bold=True, 
                                                      align="center", color=(0,0,0,255))
         self.shipY -= 35

         for ship in self.simulation.world.combatTeams[team]:
            self.drawSidebarShip(ship)
            self.shipY -= 30

         self.shipY -= 25

   def drawSidebarShip(self, ship):
      sidebarX = UserInterface.windowSize[0] - 240/2

      Sprite.draw("ship-display", position=(sidebarX, self.shipY), hud=True)

      if ship.inWorld and not ship.destroyed:
         color = (0, 0, 0, 255)

         exponentialSize = 1.0 - (1.0 / (ship.maxDeflectorPower - 1))
         deflectorWidth = 12 + (exponentialSize * (50-12))

         power = scalarBound(0, ship.availableDeflectorPower / ship.maxDeflectorPower, 1.0)
         delta = int(power * deflectorWidth)

         statusAlpha, status = ship.status
         Sprite.draw("ship-deflector", position=(UserInterface.windowSize[0] - 10 + 25 - delta, self.shipY), hud=True)

         if not ship.hasTakenDamage:
            Sprite.draw("ship-ok", position=(UserInterface.windowSize[0] - 5, self.shipY), hud=True)
         else:
            Sprite.draw("ship-damage", position=(UserInterface.windowSize[0] - 5, self.shipY), hud=True)

         statusColor = (0, 0, 0, int(scalarBound(0.2,statusAlpha,1.0)*255))

         Sprite.drawText(ship.name, position=(sidebarX - 110, self.shipY), bold=True, color=color)
         Sprite.drawText(status.lower(), position=(sidebarX - 20, self.shipY), bold=False, color=statusColor)

   def complete(self):
      return self.simulation.complete()

   def tick(self, dt):
      HUD.clear()
      self.simulation.tick()

      #if self.zoomedShip != None:
      #   Sprite.worldScale = 0.1

      #   center = vectorScale(self.zoomedShip.position, -1)
      #   center = vectorAdd(center, vectorScale(viewWindowCenter, 1.0/Sprite.worldScale))

      #   Sprite.worldPosition = center



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
