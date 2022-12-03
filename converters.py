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
		
def scale(val, src, dst):
	"""
	Scale the given value from the scale of src to the scale of dst.
	"""
	return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

def s2c(r,theta,phi):
	# spherical to cartesian conversion
	# theta = azimuth in deg (counterclockwise ordering from 0)
	# phi = elevation in deg (from 0 elevation)
	x = r * np.cos(np.radians(theta)) * np.sin(np.radians(90-phi))
	y = r * np.sin(np.radians(theta)) * np.sin(np.radians(90-phi))
	z = r * np.cos(np.radians(90-phi))
	return(x,y,z)

def lines(device,posA,posB,T):
	# Draws a line between posA and posB in time T
	# to be used in source placement
	assert type(posA) == list, 'posA is a point in 3D space'
	assert type(posB) == list, 'posA is a point in 3D space'
	nt = int(T/cfg.CLOCK)
	X = np.linspace(posA[0],posB[0],nt)
	Y = np.linspace(posA[1],posB[1],nt)
	Z = np.linspace(posA[2],posB[2],nt)
	for i in range(nt):
		device.position([X[i],Y[i],Z[i]],mode='set')
		time.sleep(cfg.CLOCK)

def circles(device,aziA,aziB,T):
	assert type(aziA) == int, 'aziA is an angle in a circle'
	assert type(aziB) == int, 'aziB is an angle in a circle'
	narc = np.abs(aziB-aziA)
	for i in range(aziA,aziB+1):
		x = 0.5+np.cos(-i*np.pi/180+np.pi/2)/2
		y = 0.5+np.sin(-i*np.pi/180+np.pi/2)/2
		z = 0.0
		time.sleep (T/narc)
		device.position([x,y,z],mode='set')