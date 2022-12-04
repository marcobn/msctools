#
# msctools: my collection of composing and performing tools in python
#
# © 2023 Marco Buongiorno Nardelli
#

import time
import numpy as np

from .converters import *
from .devices import Spat
import msctools.cfg as cfg

# Dynamics

def multiEnv(tracklist,T,omega=None):

	# general function that builds the envelope series for each individual channel
	# with a constant amplitude algorithm and arbiitrarily chosen time of flight for each channel
	# Om = list of frequencies for individual channels - determines the time spent on each speaker
	# len(OM) in input = number of channels to distribute sound to
	# T = length of the sample
	
	assert type(tracklist) == list, 'must be a list of tracks'
	if omega == None:
		omega = np.ones(len(tracklist)).tolist()
	Om = omega.copy()
	Om.append(1)
	nch = len(Om)-1
	if nch == 1:
		# trivial single channel case
		env = [np.ones(T)]
	else:
		# 2 or more channels
		sections = [0]
		for n in range(0,nch):
			sections.append(np.pi/2/Om[n])
		L = sum(sections)-sections[-1]
		x = np.linspace(0,L,int(T//cfg.CLOCK))
		env = [None]*(nch)
		ienv = [None]*(nch)
		zeroup = 0
		zerodown = 0
		for n in range(nch):
			zeroup += sections[n]
			zerodown = zeroup - sections[n]
			zeroflat = zeroup + sections[n+1]
			T = Om[n]
			Tp = Om[n-1]
			env[n] = np.cos(T*(x-zeroup))**2
			ienv[n] = np.sin((Tp)*(x-zerodown))**2
			env[n][x < zeroup] = ienv[n][x < zeroup]
			env[n][x < zerodown] = 0
			env[n][x > zeroflat] = 0
	env = scale(np.array(env),[0.0,1.0],[0.0,0.85])
	for i in range(len(x)):
		for n,tr in enumerate(tracklist):
			tr.volume(env[n][i],mode='set')
		time.sleep(cfg.CLOCK)

def crescendo(tracklist,Vini,Vend,T):
	assert type(tracklist) == list, 'must be a list of tracks'
	# input volumes in dB, time in seconds
	# set initial volume (decimal)
	Vini = db2value(Vini)
	Vend = db2value(Vend)
	assert Vini <= Vend
	track.volume(Vini,mode='set')
	nt = int(T/cfg.CLOCK)
	dV = (Vend - Vini)/nt
	V = Vini
	for t in range(nt):
		time.sleep(cfg.CLOCK)
		V += dV
		for tr in tracklist:
			tr.volume(V,mode='set')
	for tr in tracklist:
		tr.volume(Vend,mode='set')
		
def decrescendo(tracklist,Vini,Vend,T):
	assert type(tracklist) == list, 'must be a list of tracks'
	# input volumes in dB, time in seconds
	# set initial volume (decimal)
	Vini = db2value(Vini)
	Vend = db2value(Vend)
	assert Vini >= Vend
	track.volume(Vini,mode='set')
	nt = int(T/cfg.CLOCK)
	dV = (Vini - Vend)/nt
	V = Vini
	for t in range(nt):
		time.sleep(cfg.CLOCK)
		V -= dV
		for tr in tracklist:
			tr.volume(V,mode='set')
	for tr in tracklist:
		tr.volume(Vend,mode='set')
		
# Position (generic device)
		
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
		try:
			device.position([X[i],Y[i],Z[i]],mode='set')
		except:
			# for SpatGris
			device.car(X[i],Y[i],Z[i],0.0,0.0)
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
		
# SpatGris control envelopes

def circlesCar(source,aziA,aziB,radius,T):
	narc = np.abs(aziB-aziA)
	sign = np.sign(aziB-aziA)
	nt = int(T/cfg.CLOCK)
	ddeg = narc/nt
	d = aziA
	for i in range(nt+1):
		if cfg.stop_source[source]:
			break
		x = radius*np.cos(-d*np.pi/180+np.pi/2)
		y = radius*np.sin(-d*np.pi/180+np.pi/2)
		z = 0.0
		Spat(source).car(x,y,z,0.0,0.0)
		d += sign*ddeg
		time.sleep (cfg.CLOCK)

def circlesDeg(source,aziA,aziB,T):
	narc = np.abs(aziB-aziA)
	sign = np.sign(aziB-aziA)
	nt = int(T/cfg.CLOCK)
	ddeg = narc/nt
	d = aziA
	for i in range(nt+1):
		if cfg.stop_source[source]:
			break
		Spat(source).deg(d,0.0,1.0,0.0,0.0)
		d += sign*ddeg
		time.sleep(cfg.CLOCK)