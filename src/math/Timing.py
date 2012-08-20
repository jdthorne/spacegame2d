import time

times = { }
calls = { }

timing = False

def timedFunction(fn):
   def wrap(*args, **kwargs):
      start = time.clock()
      result = fn(*args, **kwargs)
      end = time.clock()
      delta = end - start
   
      name = fn.__module__ + "." + fn.__name__
      if not name in times:
         times[name] = 0.0
         calls[name] = 0
      
      times[name] += delta
      calls[name] += 1
      return result
   
   return wrap
   
def printAll():
   print
   print "Timing Results:"
   print "========================"
   for fn in sorted(times.keys(), key=lambda x: -times[x]):
      print "%10d %9.6f %s" % (calls[fn], times[fn], fn)
      
   print
   print
