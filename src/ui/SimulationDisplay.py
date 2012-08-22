import Render
import Sprite
import Scalar
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
      Sprite.draw("background", position=UserInterface.halfWindowSize, hud=True)

      self.orientWorld()
      for item in self.simulation.world.all:
         Render.render(item)

      HUD.draw(self.zoomedShip)
      self.drawSidebar()

   def drawSidebar(self):
      sidebarX = UserInterface.windowSize[0] - 240/2
      sidebarY = UserInterface.windowSize[1]/2
      Sprite.draw("sidebar", position=(sidebarX, sidebarY), hud=True)

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

         power = Scalar.bound(0, ship.availableDeflectorPower / ship.maxDeflectorPower, 1.0)
         delta = int(power * deflectorWidth)

         statusAlpha, status = ship.status
         Sprite.draw("ship-deflector", position=(UserInterface.windowSize[0] - 10 + 25 - delta, self.shipY), hud=True)

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
      HUD.clear()
      self.simulation.tick()

   def orientWorld(self):
      world = self.simulation.world 

      if self.zoomedShip != None:
         radius = Misc.WEAPON_RANGE * 0.8
         x, y = self.zoomedShip.position

         topEdge = y + radius
         bottomEdge = y - radius
         leftEdge = x - radius
         rightEdge = x + radius

         mixSpeed = 0.4

      elif len(self.simulation.shipsToJump) > 0:
         leftEdge = -Simulation.WORLD_SIZE
         rightEdge = Simulation.WORLD_SIZE

         bottomEdge = -Simulation.WORLD_SIZE
         topEdge = Simulation.WORLD_SIZE

         mixSpeed = 0.4

      else:
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
               
         padding = 2000
         xMin -= padding
         yMin -= padding
         xMax += padding
         yMax += padding

         topEdge = yMax
         bottomEdge = yMin
         leftEdge = xMin
         rightEdge = xMax

         mixSpeed = 0.05

      # Calculate scale based on edges
      xScale = 0.75*(1280-240) / abs(rightEdge - leftEdge)
      yScale = 0.75*720 / abs(topEdge - bottomEdge)
      scale = min(xScale, yScale)

      # Calculate center based on edges
      center = ( -(rightEdge + leftEdge)/2 , -(topEdge + bottomEdge)/2 )

      mixA = 1.0 - mixSpeed
      mixB = mixSpeed
      Sprite.worldScale = (mixA * Sprite.worldScale) + (mixB * scale)
      
      center = vectorAdd(center, vectorScale(viewWindowCenter, 1.0/scale))
      Sprite.worldPosition = vectorAdd(vectorScale(Sprite.worldPosition, mixA), vectorScale(center, mixB))

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
