import json

def load(name):
   filename = "./src/playerdata/fleet/%s.fleet" % (name,)
   file = open(filename).read()

   return Fleet(json.loads(file), filename)

class ShipDefinition:
   def __init__(self, data):
      self.name = data["name"]
      self.count = data["count"]
      self.design = data["design"]
      self.autopilot = data["autopilot"]

   def toDictionary(self):
      return { "name": self.name,
               "count": self.count,
               "design": self.design,
               "autopilot": self.autopilot }

class Fleet:
   def __init__(self, data, filename):
      self.name = data["name"]
      self.ships = [ShipDefinition(ship) for ship in data["ships"]]

      self.filename = filename

   def save(self):
      ships = []
      for ship in self.ships:
         ships.append(ship.toDictionary())

      dictionary = { "name": self.name,
                     "ships": ships }

      file = open(self.filename, "w")
      file.write( json.dumps(dictionary, indent=3) )
      file.close()

