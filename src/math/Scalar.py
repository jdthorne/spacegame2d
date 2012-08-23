
def scalarMix(factor, a, b):
   return (factor * a) + ((1.0-factor)*b)
   
def scalarSign(number):
   if number > 0:
      return 1
   if number < 0:
      return -1
      
   return 0

def scalarBound(min, number, max):
   if number < min:
      return min
   if number > max:
      return max
   
   return number
   