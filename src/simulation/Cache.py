
cache = {}

def cachedFunction(fn):
   def inner(*args, **kwargs):
      owner = args[0]

      key = str(fn) + str(args[0])
      if key in cache:
         return cache[key]
      else:
         result = fn(*args, **kwargs)
         cache[key] = result
         return result

   return inner

def clear():
   cache.clear()
