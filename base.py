#
# msctools: my collection of composing and performing tools in python
#
# © 2023 Marco Buongiorno Nardelli
#

import time
import numpy as np
from scipy.io import wavfile

from .osctools import client
from .converters import *
import msctools.cfg as cfg

# base classes

class Song:
	
	def __init__(self,host="127.0.0.1",port=11000):
		self.port = port
		self.host = host
		
	def start(self):
		client("/live/song/start_playing",[],self.host,self.port).send()
		
	def stop(self):
		client("/live/song/stop_playing",[],self.host,self.port).send()
		
	def test(self):
		client("/live/test",[],port=11000).send()
		
	def num(self):
		client("/live/song/get/num_tracks",[],self.host,self.port).send()
		time.sleep(cfg.TICK)
		return(cfg.data[0])
	
	def tempo(self,bpm=None,mode='set'):
		if mode == 'set':
			client("/live/song/set/tempo",[bpm],self.host,self.port).send()
		if mode == 'get':
			client("/live/song/get/tempo",[],self.host,self.port).send()
			time.sleep(cfg.TICK)
			return(cfg.data[0])
		
	def add_audio_track(self,N=0):
		client("/live/song/create_audio_track",[N],self.host,self.port).send()
		
	def del_audio_track(self,N=0):
		client("/live/song/delete_track",[N],self.host,self.port).send()
		
class Track:
	
	def __init__(self,track,host="127.0.0.1",port=11000):
		self.n = track
		self.port = port
		self.host = host
		
	def arm(self):
		client("/live/track/set/arm",[self.n,1],self.host,self.port).send()
		
	def disarm(self):
		client("/live/track/set/arm",[self.n,0],self.host,self.port).send()
		
	def volume(self,vol=db2value(0.0),mode='set'):
		if mode == 'set':
			client("/live/track/set/volume",[self.n,db2value(vol)],self.host,self.port).send()
		if mode == 'get':
			client("/live/track/get/volume",[self.n],self.host,self.port).send()
			time.sleep(cfg.TICK)
			return(value2db(cfg.data[0]))
		
	def name(self,names=None,mode='set'):
		if mode == 'set':
			client("/live/track/set/name",[self.n,names],self.host,self.port).send()
		if mode == 'get':
			client("/live/track/get/name",[self.n],self.host,self.port).send()
			time.sleep(cfg.TICK)
			return(cfg.data)
		
	def panning(self,pan=0,mode='set'):
		client("/live/track/set/panning",[self.n,pan],self.host,self.port).send()
		
	def nclips(self):
		client("/live/track/get/clips/name",[self.n],self.host,self.port).send()
		time.sleep(cfg.TICK)
		return((len(cfg.data)))
	
	def ndevices(self):
		client("/live/track/get/num_devices",[self.n],self.host,self.port).send()
		time.sleep(cfg.TICK)
		return(cfg.data[0])
	
	def devnames(self):
		client("/live/track/get/devices/name",[self.n],self.host,self.port).send()
		time.sleep(cfg.TICK)
		return(cfg.data)
	
class Clip:
	
	def __init__(self,track,clip,host="127.0.0.1",port=11000):
		self.n = track
		self.c = clip
		self.port = port
		self.host = host
		
	def name(self,names=None,mode='set'):
		if mode == 'set':
			client("/live/clip/set/name",[self.n,self.c,names],self.host,self.port).send()
		if mode == 'get':
			client("/live/clip/get/name",[self.n,self.c],self.host,self.port).send()
			time.sleep(cfg.TICK)
			return(cfg.data)
		
	def fpath(self):
		client("/live/clip/get/file_path",[self.n,self.c],self.host,self.port).send()
		return(cfg.data[0])
	
	def looping(self,mode='off'):
		if mode == 'off':
			client("/live/clip/set/looping",[self.n,self.c,0],self.host,self.port).send()
		if mode == 'on':
			client("/live/clip/set/looping",[self.n,self.c,1],self.host,self.port).send()
			
	def warping(self,mode='off'):
		if mode == 'off':
			client("/live/clip/set/warping",[self.n,self.c,0],self.host,self.port).send()
		if mode == 'on':
			client("/live/clip/set/warping",[self.n,self.c,1],self.host,self.port).send()
			
	def dur(self):
		client("/live/clip/get/file_path",[self.n,self.c],self.host,self.port).send()
		time.sleep(cfg.TICK)
		fil = cfg.data[0]
		sr, wav = wavfile.read(fil)
		nsamples = wav.size/wav.shape[1]
		return(nsamples/sr)
	
class Device:
	
	def __init__(self,track,device,controls=None,host="127.0.0.1",port=11000):
		self.n = track
		self.d = device
		self.cntr = controls
		self.port = port
		self.host = host
		
	def name(self):
		client("/live/device/get/name",[self.n,self.d],self.host,self.port).send()
		time.sleep(cfg.TICK)
		return(cfg.data[0])
	
	def num(self):
		client("/live/device/get/num_parameters",[self.n,self.d],self.host,self.port).send()
		time.sleep(cfg.TICK)
		return(cfg.data[0])
	
	def max(self):
		client("/live/device/get/parameters/max",[self.n,self.d],self.host,self.port).send()
		time.sleep(cfg.TICK)
		return(cfg.data)
	
	def min(self):
		client("/live/device/get/parameters/min",[self.n,self.d],self.host,self.port).send()
		time.sleep(cfg.TICK)
		return(cfg.data)
	
	def cntrldict(self,mode='get'):
		if mode =='get':
			client("/live/device/get/parameters/name",[self.n,self.d],self.host,self.port).send()
			time.sleep(cfg.TICK)
			keys = list(cfg.data).copy()
			client("/live/device/get/parameters/value",[self.n,self.d],self.host,self.port).send()
			time.sleep(cfg.TICK)
			values = list(cfg.data).copy()
			pardict = dict(zip(keys,values))
			assert len(pardict) == self.num(),'duplicate keys - use cntrllist method instead'
			return(pardict)
		if mode =='set':
			client("/live/device/set/parameters/value",[self.n,self.d]+list(self.cntr.values()),
				self.host,self.port).send()
			time.sleep(cfg.TICK)
			
	def cntrllist(self,mode='get'):
		if mode =='get':
			keys = []
			values = []
			for n in range(self.num()):
				time.sleep(cfg.TICK)
				client("/live/device/get/parameter/name",[self.n,self.d,n],self.host,self.port).send()
				time.sleep(cfg.TICK)
				keys.append(cfg.data[0])
			for n in range(self.num()):
				time.sleep(cfg.TICK)
				client("/live/device/get/parameter/value",[self.n,self.d,n],self.host,self.port).send()
				time.sleep(cfg.TICK)
				values.append(float(cfg.data[0]))
			return(np.array(keys),np.array(values))
		if mode =='set':
			client("/live/device/set/parameters/value",[self.n,self.d]+self.cntr,
				self.host,self.port).send()
			time.sleep(cfg.TICK)
			
	def param(self,n,val=None,mode='name'):
		if mode == 'name':
			client("/live/device/get/parameter/name",[self.n,self.d,n],self.host,self.port).send()
			time.sleep(cfg.TICK)
			return(cfg.data[0])
		if mode == 'get':
			client("/live/device/get/parameter/value",[self.n,self.d,n],self.host,self.port).send()
			time.sleep(cfg.TICK)
			return(cfg.data[0])
		if mode == 'set':
			client("/live/device/set/parameter/value",[self.n,self.d,n,val],self.host,self.port).send()
			time.sleep(cfg.TICK)