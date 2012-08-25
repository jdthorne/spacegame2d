
import sys
import imp
import math
import World
import Ship
from Vector import *
import Timing
import Fleet
import CombatTeam
import random
import Misc
import App
import CombatTeamPanel

class Simulation:
   def __init__(self, seed, fleets):
      App.world.setSeed(seed)

      for fleet in fleets:
         fleet = Fleet.load(fleet)
         team = CombatTeam.CombatTeam(fleet)

         App.world.addCombatTeam(team)
