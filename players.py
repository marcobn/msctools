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

def player(clips,track,delay=0,mode='network',external=None,nxmodel='barabasi_albert_graph',*args):
	''' 
	Play clips in sequence
	mode = "network"    : sequence defined by the eulerian path on a network
						: network models can be found here: 
						: https://networkx.org/documentation/stable/reference/generators.html
						: arguments are passed through *args
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
			mynetx = getattr(nx,nxmodel)
			Gx = mynetx(*args)
			chino = chinese_postman(Gx,None,verbose=False)
			seq = [chino[0][0]]
			for s in range(1,len(chino)):
				seq.append(chino[s][1])
				if cfg.stop_threads:
					break
		elif mode == 'sequential':
			seq = np.linspace(0,len(clips[track])-1,len(clips[track]),dtype=int).tolist()
			print(seq)
		elif mode == 'random':
			seq = np.linspace(0,len(clips[track])-1,len(clips[track]),dtype=int).tolist()
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

def playerA(clips,track,delay=0,mode='network',external=None,nxmodel='barabasi_albert_graph',*args):
	''' 
	Play clips in sequence
	mode = "network"    : sequence defined by the eulerian path on a network
						: network models can be found here: 
						: https://networkx.org/documentation/stable/reference/generators.html
						: arguments are passed through *args
	mode = "sequential" : plays the clips in descending order
	mode = "random"     : plays clips in random order
	mode = "external"   : plays clip with a user supplied sequence
	'''
	# delay the start of playback
	time.sleep(delay)
	while True:
		if cfg.stop_A:
			break
		if mode == 'network':
			mynetx = getattr(nx,nxmodel)
			Gx = mynetx(*args)
			chino = chinese_postman(Gx,None,verbose=False)
			seq = [chino[0][0]]
			for s in range(1,len(chino)):
				seq.append(chino[s][1])
				if cfg.stop_A:
					break
		elif mode == 'sequential':
			seq = np.linspace(0,len(clips[track])-1,len(clips[track]),dtype=int).tolist()
		elif mode == 'random':
			seq = np.linspace(0,len(clips[track])-1,len(clips[track]),dtype=int).tolist()
			np.random.shuffle(seq)
		elif mode == 'external':
			seq = external
		else:
			print('mode not implemented')
		for n in range(len(seq)):
			client("/live/clip/fire",[track,seq[n]],port=11000).send()
			time.sleep(clips[track][seq[n]].dur()+np.random.rand()*cfg.sleep)
			if cfg.stop_A:
				break
			
def playerB(clips,track,delay=0,mode='network',external=None,nxmodel='barabasi_albert_graph',*args):
	''' 
	Play clips in sequence
	mode = "network"    : sequence defined by the eulerian path on a network
						: network models can be found here: 
						: https://networkx.org/documentation/stable/reference/generators.html
						: arguments are passed through *args
	mode = "sequential" : plays the clips in descending order
	mode = "random"     : plays clips in random order
	mode = "external"   : plays clip with a user supplied sequence
	'''
	# delay the start of playback
	time.sleep(delay)
	while True:
		if cfg.stop_B:
			break
		if mode == 'network':
			mynetx = getattr(nx,nxmodel)
			Gx = mynetx(*args)
			chino = chinese_postman(Gx,None,verbose=False)
			seq = [chino[0][0]]
			for s in range(1,len(chino)):
				seq.append(chino[s][1])
				if cfg.stop_B:
					break
		elif mode == 'sequential':
			seq = np.linspace(0,len(clips[track])-1,len(clips[track]),dtype=int).tolist()
		elif mode == 'random':
			seq = np.linspace(0,len(clips[track])-1,len(clips[track]),dtype=int).tolist()
			np.random.shuffle(seq)
		elif mode == 'external':
			seq = external
		else:
			print('mode not implemented')
		for n in range(len(seq)):
			client("/live/clip/fire",[track,seq[n]],port=11000).send()
			time.sleep(clips[track][seq[n]].dur()+np.random.rand()*cfg.sleep)
			if cfg.stop_B:
				break

def playerC(clips,track,delay=0,mode='network',external=None,nxmodel='barabasi_albert_graph',*args):
	''' 
	Play clips in sequence
	mode = "network"    : sequence defined by the eulerian path on a network
						: network models can be found here: 
						: https://networkx.org/documentation/stable/reference/generators.html
						: arguments are passed through *args
	mode = "sequential" : plays the clips in descending order
	mode = "random"     : plays clips in random order
	mode = "external"   : plays clip with a user supplied sequence
	'''
	# delay the start of playback
	time.sleep(delay)
	while True:
		if cfg.stop_C:
			break
		if mode == 'network':
			mynetx = getattr(nx,nxmodel)
			Gx = mynetx(*args)
			chino = chinese_postman(Gx,None,verbose=False)
			seq = [chino[0][0]]
			for s in range(1,len(chino)):
				seq.append(chino[s][1])
				if cfg.stop_C:
					break
		elif mode == 'sequential':
			seq = np.linspace(0,len(clips[track])-1,len(clips[track]),dtype=int).tolist()
		elif mode == 'random':
			seq = np.linspace(0,len(clips[track])-1,len(clips[track]),dtype=int).tolist()
			np.random.shuffle(seq)
		elif mode == 'external':
			seq = external
		else:
			print('mode not implemented')
		for n in range(len(seq)):
			client("/live/clip/fire",[track,seq[n]],port=11000).send()
			time.sleep(clips[track][seq[n]].dur()+np.random.rand()*cfg.sleep)
			if cfg.stop_C:
				break
			
def playerD(clips,track,delay=0,mode='network',external=None,nxmodel='barabasi_albert_graph',*args):
	''' 
	Play clips in sequence
	mode = "network"    : sequence defined by the eulerian path on a network
						: network models can be found here: 
						: https://networkx.org/documentation/stable/reference/generators.html
						: arguments are passed through *args
	mode = "sequential" : plays the clips in descending order
	mode = "random"     : plays clips in random order
	mode = "external"   : plays clip with a user supplied sequence
	'''
	# delay the start of playback
	time.sleep(delay)
	while True:
		if cfg.stop_D:
			break
		if mode == 'network':
			mynetx = getattr(nx,nxmodel)
			Gx = mynetx(*args)
			chino = chinese_postman(Gx,None,verbose=False)
			seq = [chino[0][0]]
			for s in range(1,len(chino)):
				seq.append(chino[s][1])
				if cfg.stop_D:
					break
		elif mode == 'sequential':
			seq = np.linspace(0,len(clips[track])-1,len(clips[track]),dtype=int).tolist()
		elif mode == 'random':
			seq = np.linspace(0,len(clips[track])-1,len(clips[track]),dtype=int).tolist()
			np.random.shuffle(seq)
		elif mode == 'external':
			seq = external
		else:
			print('mode not implemented')
		for n in range(len(seq)):
			client("/live/clip/fire",[track,seq[n]],port=11000).send()
			time.sleep(clips[track][seq[n]].dur()+np.random.rand()*cfg.sleep)
			if cfg.stop_D:
				break