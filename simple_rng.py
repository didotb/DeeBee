from random import randint

#def rng()

def roll(start:int, kind:str=None, stop:int=None):
	out:int = 0
	if start <= 0 or stop <= 0:
		return f'Cannot roll {start} amount of dice with {stop} amount of sides.'
	if kind is None:
		return 'Invalid input: missing argument \'kind\''
	elif kind == 'd':
		if start <= 9999:
			return sum([randint(1,stop) for i in range(1,start+1)])
		else:
			return f'Not enough memory to calculate {str(start)} amount of dice.'
	elif kind == 'r':
		return randint(start,stop)

def mrng(amount:int):
	out = []
	for i in range(0,amount):
		while True:
			try:
				j = int("".join(map(str,[randint(1,a) for a in range(randint(1,9),randint(1,9))])))
			except ValueError:
				continue
			else:
				out.append(j)
				break
	return out