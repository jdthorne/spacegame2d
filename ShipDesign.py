#!/opt/local/bin/python


SHIP_DESIGN = {}

SHIP_DESIGN[0] = """\
    [PDP]   
     [SS]
      SS
    PDPDD 
   <CPPPDD>
    PDPDD 
      SS
     [SS]
    [PDP]   
"""

SHIP_DESIGN[0] = """\
    <>
     P
  <DPCD>
     P
    <>
"""

SHIP_DESIGN[1] = """\
   <D>
   <S>
   <SD>
   DDPP   
  SPPPDD
<CSSPPPSD>
  SPPPDD
   DDPP
   <SD>
   <S>
   <D>
"""


def allModules(type):
	# Break the design into modules
	modules = []
	
	y = 0
	for line in SHIP_DESIGN[type].split("\n"):
		x = 0
		for char in line:
			if char != " ":
				modules.append( (char, x, y) )
			x += 1
		
		y += 1
	
	# Find the computer		
	computer = [ m for m in modules if m[0] == "C" ][0]
	dx, dy = computer[1], computer[2]
	
	# Offset the modules
	modules = [ (type, x - dx, y - dy) for type, x, y in modules ]
	
	return modules
	