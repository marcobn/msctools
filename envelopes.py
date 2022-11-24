#
# msctools: my collection of composing and performing tools in python
#
# © 2023 Marco Buongiorno Nardelli
#

import numpy as np

from .converters import *
import msctools.cfg as cfg

def scale(val, src, dst):
	"""
	Scale the given value from the scale of src to the scale of dst.
	"""
	return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

def multiEnv(omega,T):

	# general function that builds the envelope series for each individual channel
	# with a constant amplitude algorithm and arbiitrarily chosen time of flight for each channel
	# Om = list of frequencies for individual channels - determines the time spent on each speaker
	# len(OM) in input = number of channels to distribute sound to
	# T = length of the sample
	
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
		x = np.linspace(0,L,int(T//cfg.TICK))
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
	return(scale(np.array(env),[0.0,1.0],[0.0,0.85]))