	
def sign(number):
	if number > 0:
		return 1
	if number < 0:
		return -1
		
	return 0

def bound(min, number, max):
	if number < min:
		return min
	if number > max:
		return max
	
	return number
	