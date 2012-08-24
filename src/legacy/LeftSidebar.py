import Sidebar

X_SHOWN = 119
X_HIDDEN = -121

class LeftSidebar(Sidebar.Sidebar):
   def __init__(self):
      Sidebar.Sidebar.__init__(self, X_SHOWN, X_HIDDEN)

      # Title Panel
      self.titlePanel = Sidebar.Panel("Identity", "0")
      self.nameItem = Sidebar.Item("Ship Name")
      self.titlePanel.items.append(self.nameItem)
      self.panels.append(self.titlePanel)

      # Structure
      self.structurePanel = Sidebar.Panel("Structural Configuration", "0")

      for module in ["Structure", "Deflector", "Plasma Cannon", "Forward Engine", "Reverse Engine"]:
         moduleItem = Sidebar.Item(module, icon="Hi")

         self.structurePanel.items.append(moduleItem)

      self.panels.append(self.structurePanel)

      # Test Tools
      self.testPanel = Sidebar.Panel("Test Environment", "0", onItemSelected=self.handleTestLaunched)
      self.testPanel.items.append(Sidebar.Item("Launch Test >"))
      self.panels.append(self.testPanel)

   def handleTestLaunched(self, item):
      if item != None:
         self.onTestLaunched()

   def isolateTestPanel(self):
      self.isolatePanel(self.testPanel)

   def cancelTestPanelIsolation(self):
      self.cancelIsolation()
      self.testPanel.clearSelection()

