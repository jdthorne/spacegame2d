import App
import Fleet
import FleetPanel
import ShipDesignerPanels
import Ship
import math
import Sprite
import CombatTeam
from Vector import *
import Misc

class FleetDesigner:

   # ================ CONSTRUCTION ======================
   def __init__(self, fleetName):
      self.testing = False
      self.fleet = Fleet.load(fleetName)

      self.setupFleetPanel()
      self.setupConstructionPanels()
      self.setupGrid()
      self.setupWorldOnFirstSimCycle()

   def setupFleetPanel(self):
      self.fleetPanel = FleetPanel.FleetPanel(self.fleet)
      App.ui.right.addPanel(self.fleetPanel)
      App.ui.right.onSelectionChanged += self.handleShipSelected

      self.currentShipDef = None
      self.currentShip = None

   def setupConstructionPanels(self):
      App.ui.left.onSelectionChanged += self.handleToolSelected

      self.floatyModule = None
      self.structuralPanel = ShipDesignerPanels.StructuralPanel()
      App.ui.left.addPanel(self.structuralPanel)

      self.autopilotPanel = ShipDesignerPanels.AutopilotPanel()
      App.ui.left.addPanel(self.autopilotPanel)

      self.testingPanel = ShipDesignerPanels.TestingPanel()
      App.ui.left.addPanel(self.testingPanel)

   def setupGrid(self):
      self.grid = {}
      for x in [-2, -1, 0, 1, 2]:
         for y in [-2, -1, 0, 1, 2]:
            self.grid[ (x*400, y*400) ] = Sprite.Sprite("grid", camera=App.worldCamera, layer=Sprite.gridLayer)

   def setupWorld(self, world=None):
      App.world.onUpdate -= self.setupWorld

      position = (0, 0)
      self.shipsByDefinition = {}
      for definition in self.fleet.ships:
         ship = Ship.Ship(definition, position=position, 
                                      rotation=math.pi/2,
                                      velocity=(0, 0), 
                                      combatTeam=None)
         ship.physicsEnabled = False
         ship.installAutopilot(None)
         App.world.addObject(ship)
         self.shipsByDefinition[definition] = ship

         if self.currentShipDef is definition:
            self.currentShip = ship

         position = vectorAdd(position, (Misc.WEAPON_RANGE, 0))

   # ================ WORLD HANDLING =============================
   def setupWorldOnFirstSimCycle(self):
      App.world.onUpdate += self.setupWorld

   def clearWorld(self):
      App.world.clearAll()
      App.world.simulate()

   # ================ GRID CONFIGURATION & DATA ==================
   def moveGrid(self, position):
      for delta in self.grid:
         self.grid[delta].setPosition( vectorAdd(position, delta) )

   def hideGrid(self):
      for delta in self.grid:
         self.grid[delta].hide()

   def positionToGridCoordinates(self, position):
      positionOffset = vectorSub(position, self.grid[ (0, 0) ].position)
      positionOffsetInGridCoordinates = vectorScale(positionOffset, 1.0/Misc.MODULE_SIZE)

      positionOffsetInGridCoordinates = vectorRound(positionOffsetInGridCoordinates)

      return positionOffsetInGridCoordinates      

   def snapToGrid(self, position):
      positionOffsetInGridCoordinates = self.positionToGridCoordinates(position)

      positionOffset = vectorScale(positionOffsetInGridCoordinates, Misc.MODULE_SIZE)
      position = vectorAdd(positionOffset, self.grid[ (0, 0) ].position)

      return position

   # ==================== SHIP SELECTION =========================
   def handleShipSelected(self, sidebar, item):
      if item == None or (not "shipDef" in item.__dict__):
         self.currentShip = None
         self.currentShipDef = None

         App.ui.left.deselectAll()
         App.ui.left.hide()
         App.worldCamera.focus = None
         self.handleToolSelected()
         return

      if item.shipDef is self.currentShipDef:
         return

      self.cancelTest()

      ship = self.shipsByDefinition[item.shipDef]

      self.currentShipDef = item.shipDef
      self.currentShip = ship
      App.ui.left.show()
      App.worldCamera.focus = ship
      App.worldCamera.focusScale = 1.0

      self.autopilotPanel.display(item.shipDef.autopilot)

      self.handleToolSelected()

   # ==================== TOOL SELECTION =========================
   def handleToolSelected(self, sidebar=None, tool=None):
      if self.testingPanel.isLaunchRequested():
         self.launchTest()
      else:
         self.cancelTest()

      self.updateSelectedStructuralTool()

   # ==================== STRUCTURAL TOOL =========================
   def updateSelectedStructuralTool(self):
      module = self.structuralPanel.selectedToolSprite()

      if (module == None) or (self.currentShip == None):
         self.hideGrid()

         if self.floatyModule != None:
            self.floatyModule.destroy()
            self.floatyModule = None

         return

      self.moveGrid(self.currentShip.flightComputer.absolutePosition())
      self.floatyModule = Sprite.Sprite(module, camera=App.worldCamera, rotation=math.pi/2, layer=Sprite.toolLayer)

   def handleMouseMoved(self, x, y, dx, dy):
      if self.floatyModule == None:
         return

      if abs(x) >= (App.ui.windowCenter[0] - 240):
         self.floatyModule.hide()
         return

      worldPosition = App.worldCamera.toWorldCoordinates( (x, y) )

      position = self.snapToGrid( App.worldCamera.toWorldCoordinates( (x, y) ))
      self.floatyModule.setPosition(position)

   def handleMouseDown(self, x, y, button, modifiers):
      if abs(x) >= (App.ui.windowCenter[0] - 240):
         return

      if self.floatyModule != None:
         module = self.structuralPanel.selectedToolIdentifier()
         position = App.worldCamera.toWorldCoordinates( (x, y) )
         position = self.positionToGridCoordinates( position )
         position = vectorRound(vectorRotate(position, -math.pi/2))

         self.currentShip.installModule(module, position)
         self.currentShipDef.design = self.currentShip.design()
         self.fleet.save()

   # ================= TESTING SCENARIO =====================
   def launchTest(self):
      if self.testing:
         return

      self.testing = True
      self.clearWorld()
      App.worldCamera.focusScale = 0.1

      # Create the local combat team
      CombatTeam.nextTeamId = 0
      localCombatTeam = CombatTeam.BasicCombatTeam(self.currentShip.name)

      ship = Ship.Ship(self.currentShipDef, self.currentShip.position, 
                       math.pi/2, (0, 0), localCombatTeam)
      localCombatTeam.addShip(ship)

      App.world.addCombatTeam(localCombatTeam)

      # Add the ship to the new world
      localCombatTeam.shipsInWorld.append(ship)
      App.world.addObject(ship)
      self.currentShip = ship
      App.worldCamera.focus = ship

      # Add the enemy team
      enemyTeam = CombatTeam.CombatTeam(Fleet.load("james-swarm"))
      App.world.addCombatTeam(enemyTeam)

   def cancelTest(self):
      if not self.testing:
         return

      self.testing = False

      if self.testingPanel.isLaunchRequested:
         App.ui.left.deselectAll()

      self.clearWorld()
      self.setupWorld()

      App.worldCamera.focusScale = 1.0
      App.worldCamera.focus = self.currentShip

