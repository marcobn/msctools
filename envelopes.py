#
# msctools: my collection of composing and performing tools in python
#
# © 2023 Marco Buongiorno Nardelli
#

import time
import numpy as np

from .converters import *
import msctools.cfg as cfg

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

def crescendo(track,Vini,Vend,T):
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
		track.volume(V,mode='set')
	track.volume(Vend,mode='set')
		
def decrescendo(track,Vini,Vend,T):
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
		track.volume(V,mode='set')
	track.volume(Vend,mode='set')

		
		
	
	