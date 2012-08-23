import json

def load(name):
   file = open("./src/playerdata/fleet/%s.fleet" % (name,)).read()

   return Fleet(json.loads(file))

class ShipDefinition:
   def __init__(self, data):
      self.name = data["name"]
      self.count = data["count"]
      self.design = data["design"]
      self.autopilot = data["autopilot"]

class Fleet:
   def __init__(self, data):
      self.name = data["name"]
      self.ships = [ShipDefinition(ship) for ship in data["ships"]]



