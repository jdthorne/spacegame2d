swarmship = """\
   <PP>
  <PCPDP>
   <PP>
"""

ships = []
for i in range(16):
  ships.append( ("Swarm %d" % (i,), swarmship) )

def fleet():
  return ships
