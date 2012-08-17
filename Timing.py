import time

functions = { }

timing = False

def timedFunction(friendlyName="(Unnamed Function)"):
	if (not timing) and ("/" in friendlyName):
		return lambda x: x
		
	def timedFunctionCore(fn):
		def wrap(*args, **kwargs):
			start = time.clock()
			result = fn(*args, **kwargs)
			end = time.clock()
			delta = end - start
		
			name = friendlyName
			if not name in functions:
				functions[name] = 0.0
			
			functions[name] += delta
			return result
		
		return wrap
		
	return timedFunctionCore
	
def printAll():
	print
	print "Timing Results:"
	print "========================"
	for fn in sorted(functions.keys()):
		print "%9.6f %s" % (functions[fn], fn)
		
	print
	print
