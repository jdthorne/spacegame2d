	
def Sign(number):
	if number > 0:
		return 1
	if number < 0:
		return -1
		
	return 0

def Bound(min, number, max):
	if number < min:
		return min
	if number > max:
		return max
	
	return number
	