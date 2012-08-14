#!/opt/local/bin/python


SHIP_DESIGN = """\
     []
    <SSSCS
     []
"""


def AllModules():
	# Break the design into modules
	modules = []
	
	y = 0
	for line in SHIP_DESIGN.split("\n"):
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
	