import Sidebar
import Sprite
from Vector import *

class StructuralPanel(Sidebar.Panel):
   def __init__(self):
      Sidebar.Panel.__init__(self, "Structural Configuration", "0")

      self.tools = {}
      for module in ["Structure", "Deflector", "Plasma Cannon", "Forward Engine", "Reverse Engine", "Delete"]:
         item = Sidebar.Item()
         item.nameText.setText(module)
         self.tools[item] = module
         self.items.append(item)

      self.toolImageNames = { "Structure": "structure-0",
                              "Deflector": "deflector",
                              "Plasma Cannon": "plasma-cannon",
                              "Forward Engine": "engine-structure",
                              "Reverse Engine": "engine-structure@180",
                              "Delete": "plasma" }

      self.toolIdentifiers = { "Structure": "S",
                               "Deflector": "D",
                               "Plasma Cannon": "P",
                               "Forward Engine": "<",
                               "Reverse Engine": ">",
                               "Delete": " " }

   def selectedTool(self):
      for item in self.items:
         if item.selected:
            return self.tools[item]

      return None

   def selectedToolSprite(self):
      if self.selectedTool() == None:
         return None

      return self.toolImageNames[self.selectedTool()]

   def selectedToolIdentifier(self):
      if self.selectedTool() == None:
         return None

      return self.toolIdentifiers[self.selectedTool()]

class AutopilotPanel(Sidebar.Panel):
   def __init__(self):
      Sidebar.Panel.__init__(self, "Flight Computer", "0")

      self.select = Sidebar.Item("Autopilot", right="...")
      self.items.append(self.select)

      self.edit = Sidebar.Item("Edit Autopilot Source", right="->")
      self.items.append(self.edit)

   def display(self, text):
      self.select.statusText.setText(text)

class TestingPanel(Sidebar.Panel):
   def __init__(self):
      Sidebar.Panel.__init__(self, "Testing", "0")

      self.environment = Sidebar.Item("Scenario", "crates", right="...")
      self.items.append(self.environment)

      self.launch = Sidebar.Item("Enter Test Environment", right="->")
      self.items.append(self.launch)

   def isLaunchRequested(self):
      return self.launch.selected
      