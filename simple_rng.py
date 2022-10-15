import re, operator
from random import randint
from collections import deque

dicelist = {'d','r','z'}

def roll(start:int, kind:str=None, stop:int=None):
	out:int = 0
	if start <= 0 or stop <= 0:
		return {'error':True, 'value':f'Cannot roll {start} amount of dice with {stop} amount of sides.'}
	if kind is None:
		return {'error':True, 'value':'Invalid input: missing argument \'kind\''}
	if kind == 'd' or kind == 'z':
		if start > 9999:
			return {'error':True, 'value':f'Not enough memory to calculate {str(start)} amount of dice.'}
		return [randint(1,stop) for i in range(1,start+1)] if kind == 'd' else [randint(0,stop) for i in range(1,start+1)]
	elif kind == 'r':
		if start > stop:
			start, stop = stop, start
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

def roll_parser(dice_notation:str=None):
	if dice_notation is not None:
		dice = dice_notation.lower()
		valid_ops = set('+-*/') # Parsing operation by stackoverflow:mgilson
		ops, nums, buff = [],[],[] # Parsing operation by stackoverflow:mgilson
		op_order = ('*/','+-')
		op_dict = {'*':operator.mul,'/':operator.truediv,'+':operator.add,'-':operator.sub}
		value = None
		try:
			divd = deque([int(temp) if temp.isdigit() else temp for temp in re.match(r'([a-z]+)([0-9]+)([+,-,*,/][0-9]+)',dice).groups()])
			divd.appendleft(1)
		except AttributeError:
			try:
				divd = deque([int(temp) if temp.isdigit() else temp for temp in re.match(r'([0-9]+)([a-z]+)([0-9]+)([+,-,*,/][0-9]+)',dice).groups()])
			except AttributeError:
				try:
					divd = deque([int(temp) if temp.isdigit() else temp for temp in re.match(r'([a-z]+)([0-9]+)',dice).groups()])
					divd.appendleft(1)
				except AttributeError:
					try:
						divd = deque([int(temp) if temp.isdigit() else temp for temp in re.match(r'([0-9]+)([a-z]+)([0-9]+)',dice).groups()])
					except AttributeError:
						return {'error':True, 'value':f"Bad argument: Invalid input.\nUse dice notation."}
		if divd[1] not in dicelist:
			return {'error':True, 'value':f"BadArgument: Invalid dice type.\n\'{divd[1]}\' is not a valid type of dice."}

		initial = roll(divd[0],divd[1],divd[2])

		if isinstance(initial, dict):
			return initial
		if isinstance(initial, int):
			return {'error':False, 'value':initial, 'prev':initial}
		if len(divd) == 3:
			return {'error':False, 'value':sum(initial), 'prev':initial}
		final = ''.join([str(sum(initial)),divd[3]])
		for c in final: # Parsing operation by stackoverflow:mgilson
			if c in valid_ops:
				nums.append(''.join(buff))
				buff.clear()
				ops.append(c)
			else:
				buff.append(c)
		nums.append(''.join(buff))
		for op in op_order: # Operation evaluation by stackoverflow:mgilson
			while any(o in ops for o in op):
				idx,oo = next((i,o) for i,o in enumerate(ops) if o in op)
				ops.pop(idx)
				values = map(float,nums[idx:idx+2])
				value = op_dict[oo](*values)
				nums[idx:idx+2] = [value]
		final = nums[0]
		return {'error':False, 'value':final, 'initial':sum(initial), 'prev':initial}
