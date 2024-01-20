#
# msctools: my collection of composing and performing tools in python
#
# © 2023 Marco Buongiorno Nardelli
#
### Read the samples and create the dictionaries

import glob,time
import numpy as np
import pyo

import threading
import numpy as np
import networkx as nx

from .networks import *

import msctools.cfg as cfg

def playerP(clips=None,track=0,delay=0.0,offset=1.0,panning=None,gain=1.0,reverb=[0.50,0.51],
            mode='network',external=None,nxmodel='barabasi_albert_graph',*args):
    ''' 
    Play clips in sequence waiting for next clip in following mode
    mode = "network"    : sequence defined by the eulerian path on a network
                        : network models can be found here: 
                        : https://networkx.org/documentation/stable/reference/generators.html
                        : arguments are passed through *args
    mode = "sequential" : plays the clips in descending order
    mode = "random"     : plays clips in random order
    mode = "external"   : plays clip with a user supplied sequence
    '''

    if clips == None:
        return('no clips provided')
    time.sleep(offset)
    while True:
        if cfg.stop[track]:
            break
        if mode == 'network':
            mynetx = getattr(nx,nxmodel)
            Gx = mynetx(*args)
            chino = chinese_postman(Gx,None,verbose=False)
            seq = [chino[0][0]]
            for s in range(1,len(chino)):
                seq.append(chino[s][1])
                if cfg.stop[track]:
                    break
        elif mode == 'sequential':
            seq = np.linspace(0,len(clips)-1,len(clips),dtype=int).tolist()
        elif mode == 'random':
            seq = np.linspace(0,len(clips)-1,len(clips),dtype=int).tolist()
            np.random.shuffle(seq)
        elif mode == 'external':
            seq = external
        else:
            print('mode not implemented')
        for n in range(len(seq)):
            # set panning
            if panning == 'random':
                pan = np.random.rand()
            elif isinstance(panning,float) or isinstance(panning,int):
                pan = panning
            elif panning == 'LR':
                pan = pyo.SigTo(value=1.0, time=pyo.sndinfo(clips[n])[1], init=0.0)
            elif panning == 'RL':
                pan = pyo.SigTo(value=0.0, time=pyo.sndinfo(clips[n])[1], init=1.0)
            else:
                print('panning not defined')
            snd = pyo.SfPlayer(clips[seq[n]])
            rev = pyo.Freeverb(snd,size=reverb)
            panout = pyo.SPan(rev,outs=2,pan=pan,mul=gain).out()
            time.sleep(pyo.sndinfo(clips[seq[n]])[1]+delay*np.random.rand())
            snd.stop()
            if cfg.stop[track]:
                break

						
def scorePlayer(clips,track,score,delay=0,hold=False):
	''' 
	Play clips in sequence according to a score read as musicxml (pitch + duration)
	score[0] = pitches
	score[1] = durations in units of quantization (usually 1/4 if not specified otherwise)
	'''
	# delay the start of playback - if for any reason is desired
	time.sleep(delay)
	while True:
		if cfg.stop[track]:
			break
		seq = score[0]
		dur = score[1]
		for n in range(len(seq)):
			client("/live/clip/fire",[track,seq[n]],port=11000).send()
			if hold:
				tsleep = np.max([np.abs(60.0/cfg.tempo*cfg.beat[track]*dur[n]+(2*np.random.rand()-1)*cfg.sleep[track]),
								np.abs(clips[track][seq[n]].dur()+np.random.rand()*cfg.sleep[track])])
				time.sleep(tsleep)
			else:
				tsleep = np.abs(60.0/cfg.tempo*cfg.beat[track]*dur[n]+(2*np.random.rand()-1)*cfg.sleep[track])
				time.sleep(tsleep)
			if cfg.stop[track]:
				break

def scorePlayerP(clips,track,score,offset=0,panning=0.5,reverb=[0.51,0.52],gain=1.0,scaledur=1.0):
    ''' 
    Play clips in sequence according to a score (pitch + duration)
    score[0] = pitches
    score[1] = durations in seconds (can be scaled with the scaledur parameter)
    '''
    # delay the start of playback - if for any reason is desired
    time.sleep(offset)
    while True:
        if cfg.stop[track]:
            break
        seq = score[0]
        dur = score[1]
        for n in range(len(seq)):
            # set panning
            if panning == 'random':
                pan = np.random.rand()
            elif isinstance(panning,float) or isinstance(panning,int):
                pan = panning
            else:
                print('panning not defined')
            fade = pyo.Fader(fadein=0.1, fadeout=0.2, dur=dur[n]*scaledur).play()
            snd = pyo.SfPlayer(clips[seq[n]],mul=gain)
            rev = pyo.Freeverb(snd,size=reverb)
            panout = pyo.SPan(rev,outs=2,pan=pan,mul=fade).out()
            time.sleep(dur[n]*scaledur)
            snd.stop()
            if cfg.stop[track]:
                break

def playScene(scene,session,delay=0):
	# play a scene from the session view
	time.sleep(delay)
	for n in range(session.num_tracks()):
		client("/live/clip_slot/fire",[n,scene],cfg.HOST,cfg.PORT).send()

def importSoundfiles(dirpath='./',filepath='./',mult=0.1,gain=1.0):
	# reading wavefiles
	try:
		obj = [None]*len(glob.glob(dirpath+filepath))
		fil = [None]*len(glob.glob(dirpath+filepath))
		for file in glob.glob(dirpath+filepath):
			i = int(file.split('.')[3])
			fil[i] = file
			obj[i] = pyo.SfPlayer(file,mul=mult*gain).stop()
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
			obj0[i] = pyo.SfPlayer(file,mul=mult*gain).stop()
			obj1[i] = pyo.SfPlayer(file,mul=mult*gain).stop()
	except:
		print('error in file reading')
		pass
	
	return(obj0,obj1,fil)

def importClips(dirpath='./',filepath='./'):
	# reading wavefiles
    try:
        clips = [None]*len(glob.glob(dirpath+filepath))
        for i,file in enumerate(glob.glob(dirpath+filepath)):
            clips[i] = file
        return(clips)
    except:
        print('error in file reading')
        return

### function to distribute sounds in stereo pairs

def panMove(snd0,snd1,fil,nch,mult):
	if snd0.isPlaying() == True:
		pass
	else:
		snd0.play()
		snd1.play()
		ff = float(1/pyo.sndinfo(fil)[1]/4)
		sin = pyo.Sine(freq=ff,phase=0)
		cos = pyo.Sine(freq=ff,phase=0.25)
		ini = np.random.randint(0,nch)
		step = np.random.randint(0,int(nch/2)+1)
		end = (ini+step)%nch
		snd0.out(ini,0).setMul(mult*cos**2)
		snd1.out(end,0).setMul(mult*sin**2)
		snd0.stop(wait=pyo.sndinfo(fil)[1])
		snd1.stop(wait=pyo.sndinfo(fil)[1])
		
### function to distribute sounds in a multichannel environment

def playChannel(snd,fil,nch,mult):
	# play single wav file on channel nch
	if snd.isPlaying() == True:
		pass
	else:
		snd.play()
		snd.out(nch,0).setMul(mult)
		snd.stop(wait=pyo.sndinfo(fil)[1])

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
	snd = pyo.SndTable(sndfile)
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
		table[i] = pyo.DataTable(size=T, init=wave[i])
	return(table,freq,dur)

def chPath(chpath,table,freq,dur,mult):
	a = [None]*len(chpath)
	for i,cn in enumerate(chpath):
		a[i] = pyo.Osc(table=table[i], freq=[freq,freq], mul=mult).out(cn-1,0)
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
		granEnv = pyo.TableRead(table = pyo.WinTable(self.window), freq = granSizeRecip)
	
		# Play the live signal to granulate. This does not directly sound any audio since the
		# grain envelopes attenuate the live signal.
		self.signal.play()
		self.signal.setMul(granEnv)
	
		while True:
			if self.stopSignalGran == True:
				break
	
				# For each possible grain, determine if a grain should play based on density.
				# Each "grain" is not a sound but an envelope of the signal played above.
			granProb = np.random.uniform(0.0, 100.0) # Generate a random value as a percentage
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