import Fleet
import UserInterface
import Ship
import World
import Render
import math
import Sprite
import Simulation
import Misc

class NullAutopilot:
   def __init__(self, ship):
      pass
   def run(self):
      pass
   def status(self):
      pass 

class FleetDesigner:
   def __init__(self, fleetName):
      UserInterface.rightSidebar.show()

      self.world = World.World()
      self.fleet = Fleet.load(fleetName)

      self.ships = []
      x = 0
      for definition in self.fleet.ships:
         ship = Ship.Ship(definition.name, definition.design, NullAutopilot,
                          (x, 0), math.pi/2, (0, 0), self.world, 0)

         ship.definition = definition
         ship.status = definition.autopilot
         ship.availableDeflectorPower = 0.0
         ship.ftlTime = 0

         self.world.prepareObject(ship)
         self.world.addObject(ship)

         self.ships.append(ship)

         x += 2000

      UserInterface.leftSidebar.onTestLaunched = self.handleTestLaunched
      UserInterface.leftSidebar.layout()

      UserInterface.rightSidebar.onShipSelected = self.handleShipSelected
      UserInterface.rightSidebar.displayFleet(self.fleet, self.ships, "0")
      UserInterface.rightSidebar.layout()

      self.currentShip = None
      self.simulation = None

   def draw(self):
      if self.simulation == None:
         Sprite.orientWorld(self.world, self.currentShip, padding=500)
         Render.render(self.world)

      else:
         Sprite.orientWorld(self.world, self.currentShip)
         Render.render(self.simulation.world)

   def tick(self, dt):
      if self.simulation != None:
         self.simulation.tick()

   def handleMouseMotion(self, x, y, dx, dy):
      pass

   def complete(self):
      return False

   def handleShipSelected(self, ship):
      if self.simulation != None:
         return

      self.currentShip = ship

      if ship != None:
         UserInterface.leftSidebar.show()
      else:
         UserInterface.leftSidebar.hide()

   def handleTestLaunched(self):
      if self.simulation == None:
         self.currentShip.availableDeflectorPower = self.currentShip.maxDeflectorPower

         self.simulation = Simulation.Simulation(seed="waffle", 
                                                 fleets=[Fleet.load("james-swarm")],
                                                 existingShips=[self.currentShip])

         self.currentShip.installAutopilot(self.simulation.loadAutopilot(self.currentShip.definition.autopilot))
         UserInterface.leftSidebar.isolateTestPanel()

      else:
         self.simulation = None
         UserInterface.leftSidebar.cancelTestPanelIsolation()
         Render.clean()
