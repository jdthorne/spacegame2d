#!/opt/local/bin/python


SHIP_DESIGN = {}

SHIP_DESIGN[0] = """\
   
    []
     R
     DRD  
    <CRRD>
     DRD  
     R
    []
"""

SHIP_DESIGN[1] = """\
    <>
    S
    S
    D    
   RRRD
<CSSRRR>
   RRRD
    D
    S
    S
    <>
"""


def AllModules(type):
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
	