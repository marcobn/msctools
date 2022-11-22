#
# msctools: my collection of composing and performing tools in python
#
# © 2023 Marco Buongiorno Nardelli
#

import numpy as np

def db2value(db):
	# conversion from decibel to linear scale in track volume
	if db <= 6 and db >= -18:
		return (db+34)/40
	elif db < -18 and db >= -41:
		alpha = 799.503788
		beta = 12630.61132
		gamma = 201.871345
		delta = 399.751894
		return -(np.sqrt(-alpha*db - beta) - gamma) / delta
	elif db < -41:
		alpha = 70.
		beta = 118.426374
		gamma = 7504./5567.
		return np.power(((db+alpha)/beta),gamma)
	else:
		print('out of bounds')
		
def value2db(vl):
	# conversion from linear to decibel scale in track volume
	if vl <= 1 and vl >= 0.4:
		return 40*vl -34
	elif vl < 0.4 and vl >= 0.15:
		alpha = 799.503788
		beta = 12630.61132
		gamma = 201.871345
		delta = 399.751894
		return -((delta*vl - gamma)**2 + beta)/alpha
	elif vl < 0.15:
		alpha = 70.
		beta = 118.426374
		gamma = 7504./5567.
		return beta*np.power(vl,1/gamma) - alpha
	else:
		print('out of bounds')
		
def db4value(db):
	# conversion from decibel to linear scale in clip gain
	db -= 18
	if db <= 6 and db >= -18:
		return (db+34)/40
	elif db < -18 and db >= -41:
		alpha = 799.503788
		beta = 12630.61132
		gamma = 201.871345
		delta = 399.751894
		return -(np.sqrt(-alpha*db - beta) - gamma) / delta
	elif db < -41:
		alpha = 70.
		beta = 118.426374
		gamma = 7504./5567.
		return np.power(((db+alpha)/beta),gamma)
	else:
		print('out of bounds')
