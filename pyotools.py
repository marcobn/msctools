#
# msctools: my collection of composing and performing tools in python
#
# © 2023 Marco Buongiorno Nardelli
#
### Read the samples and create the dictionaries

import glob,time
import numpy as np
import pyo as po

def importSoundfiles(dirpath='./',filepath='./',mult=0.1,gain=1.0):
	# reading wavefiles
	try:
		obj = [None]*len(glob.glob(dirpath+filepath))
		fil = [None]*len(glob.glob(dirpath+filepath))
		for file in glob.glob(dirpath+filepath):
			i = int(file.split('.')[3])
			fil[i] = file
			obj[i] = po.SfPlayer(file,mul=mult*gain).stop()
	except:
		print('error in file reading')
		pass
	
	return(obj,fil)

def importSoundfiles2(dirpath='./',filepath='./',mult=0.1,gain=1.0):
	# reading wavefiles
	try:
		obj0 = [None]*len(glob.glob(dirpath+filepath))
		obj1 = [None]*len(glob.glob(dirpath+filepath))
		fil = [None]*len(glob.glob(dirpath+filepath))
		for file in glob.glob(dirpath+filepath):
			i = int(file.split('.')[3])
			fil[i] = file
			obj0[i] = po.SfPlayer(file,mul=mult*gain).stop()
			obj1[i] = po.SfPlayer(file,mul=mult*gain).stop()
	except:
		print('error in file reading')
		pass
	
	return(obj0,obj1,fil)

### function to distribute sounds in stereo pairs

def panMove(snd0,snd1,fil,nch,mult):
	if snd0.isPlaying() == True:
		pass
	else:
		snd0.play()
		snd1.play()
		ff = float(1/po.sndinfo(fil)[1]/4)
		sin = po.Sine(freq=ff,phase=0)
		cos = po.Sine(freq=ff,phase=0.25)
		ini = np.random.randint(0,nch)
		step = np.random.randint(0,int(nch/2)+1)
		end = (ini+step)%nch
		snd0.out(ini,0).setMul(mult*cos**2)
		snd1.out(end,0).setMul(mult*sin**2)
		snd0.stop(wait=po.sndinfo(fil)[1])
		snd1.stop(wait=po.sndinfo(fil)[1])
		
### function to distribute sounds in a multichannel environment

def playChannel(snd,fil,nch,mult):
	# play single wav file on channel nch
	if snd.isPlaying() == True:
		pass
	else:
		snd.play()
		snd.out(nch,0).setMul(mult)
		snd.stop(wait=po.sndinfo(fil)[1])

def multiEnv(ch,T):
	n = ch-1
	if n == 0:
		env = [np.ones(T)]
	else:
		t = np.linspace(0,T-1,T)
		env = [None]*ch
		for i in range(0,n+1):
			env[i] = np.sin(np.pi/2/T*n*t-(i-1)*np.pi/2)**2
			env[i][t<=(i-1)*T/n] = 0
			env[i][t>=(i+1)*T/n] = 0
	return(env)

def multiTable(sndfile,chpath):
	snd = po.SndTable(sndfile)
	T = snd.getSize()[0]
	freq = snd.getRate()
	ch = len(chpath)
	env = multiEnv(ch,snd.getSize()[0])
	wav = snd.getEnvelope(T)
	dur = snd.getDur()
	wave = [None]*ch
	table = [None]*ch
	for i in range(ch):
		tmp = np.array(wav)*env[i]
		wave[i] = tmp.tolist()
	for i,cn in enumerate(chpath):
		table[i] = po.DataTable(size=T, init=wave[i])
	return(table,freq,dur)

def chPath(chpath,table,freq,dur,mult):
	a = [None]*len(chpath)
	for i,cn in enumerate(chpath):
		a[i] = po.Osc(table=table[i], freq=[freq,freq], mul=mult).out(cn-1,0)
		a[i].stop(wait=dur)
		
class signalGran():
	
	# class written by Connor Scroggins, UNT 2023.
	
	def __init__(self, signal, mul = 1.0, granSize = 0.1, granDens = 30, window = 7):
		self.signal = signal
		self.isPlaying = 0
		self.stopSignalGran = False
		self.mul = mul
		self.granSize = granSize
		self.granDens = granDens
		self.window = window
	
	# granSignal
	#
	# Granulate a given live signal.
	#
	# input:
	# -signal: the live audio signal to granulate
	# -chan: the channel to output the granulator from
	# -granSize: the duration of each grain in seconds
	# -granDens: the density of grains as a percentage
	# -window: window type corresponding with WinTable types
	#
	# output:
	# -1 channel of live granulated audio output
	
	def playSample (self):
	
		# Take the reciprocal of the granSize since the TableRead below will use this value,
		# but TableRead uses the value for playback rate in its "freq" parameter.
		granSizeRecip = 1 / self.granSize
	
		# Generate the grain window including its duration.
		granEnv = TableRead(table = WinTable(self.window), freq = granSizeRecip)
	
		# Play the live signal to granulate. This does not directly sound any audio since the
		# grain envelopes attenuate the live signal.
		self.signal.play()
		self.signal.setMul(granEnv)
	
		while True:
			if self.stopSignalGran == True:
				break
	
				# For each possible grain, determine if a grain should play based on density.
				# Each "grain" is not a sound but an envelope of the signal played above.
			granProb = uniform(0.0, 100.0) # Generate a random value as a percentage
			if granProb <= self.granDens: # Play an if the random value is "within" the density value.
				granEnv.play()
	
			time.sleep(self.granSize) # Do not start the next grain until the current grain envelope ends.
	
	def out(self,n=0,m=1):
	
		# Check if granulator is playing.
		if self.isPlaying == 0:
			self.play()
	
		self.signal.out(n,n+m)
	
	def stop(self):
		self.signal.stop()
		self.isPlaying = 0
		self.stopSignalGran = 1
		
	def play(self):
		threading.Thread(target=self.playSample,args=()).start()
		self.isPlaying = 1
		
		
	def setSignal(self, newSignal):
		self.signal = newSignal
	
	# def setChnl(self, newChnl):
	#   self.chnl = newChnl
		
	def setMul (self, newMul):
		self.mul = newMul
	
	def setGranSize (self, newGranSize):
		self.granSize = newGranSize
		
	def setGranDens (self, newGranDens):
		self.granDens = newGranDens
	
	def setWindow (self, newWindow):
		self.window = newWindow