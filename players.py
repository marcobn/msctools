#
# msctools: my collection of composing and performing tools in python
#
# © 2023 Marco Buongiorno Nardelli
#

import time
import numpy as np
import networkx as nx

from .networks import *
from .osctools import client

import msctools.cfg as cfg

def player(clips,track,mode='network',external=None,delay=0):
	''' 
	Play clips in sequence
	mode = "network"    : sequence defined by the eulerian path on a network
	mode = "sequential" : plays the clips in descending order
	mode = "random"     : plays clips in random order
	mode = "external"   : plays clip with a user supplied sequence
	'''
	# delay the start of playback
	time.sleep(delay)
	while True:
		if cfg.stop_threads:
			break
		if mode == 'network':
			Gx = nx.barabasi_albert_graph(len(clips[track]),2)
			chino = chinese_postman(Gx,None,verbose=False)
			seq = [chino[0][0]]
			for s in range(1,len(chino)):
				seq.append(chino[s][1])
				if cfg.stop_threads:
					break
		elif mode == 'sequential':
			seq = np.linspace(0,len(dur)-1,len(clips[track]),dtype=int)
		elif mode == 'random':
			seq = np.linspace(0,len(dur)-1,len(clips[track]),dtype=int)
			np.random.shuffle(seq)
		elif mode == 'external':
			seq = external
		else:
			print('mode not implemented')
		for n in range(len(seq)):
			client("/live/clip/fire",[track,seq[n]],port=11000).send()
			time.sleep(clips[track][seq[n]].dur()+np.random.rand()*cfg.sleep)
			if cfg.stop_threads:
				break