#
# msctools: my collection of composing and performing tools in python
#
# © 2023 Marco Buongiorno Nardelli
#

# container functions

import time

from .base import *

def trackList(session):
	num_tracks = session.num()
	tracks = []
	for t in range(num_tracks):
		tracks.append(Track(t))
	time.sleep(0.01)
	return(tracks)

def clipList(session,tracks):
	num_tracks = session.num()
	num_clips = []
	for n in range(num_tracks):
		num_clips.append(tracks[n].nclips())
	clips = []
	for n in range(num_tracks):
		clp = []
		for i in range(num_clips[n]):
			clp.append(Clip(n,i))
		clips.append(clp)
	time.sleep(0.1)
	return(clips)

def deviceList(session,tracks):
	num_tracks = session.num()
	num_devices = []
	for n in range(num_tracks):
		num_devices.append(tracks[n].ndevices())
	devices = []
	for n in range(num_tracks):
		dvc = []
		for i in range(num_devices[n]):
			dvc.append(Device(n,i))
		devices.append(dvc)
	time.sleep(0.1)
	return(devices)

def setSession():
	session = Song()
	tracks = trackList(session)
	clips = clipList(session,tracks)
	devices = deviceList(session,tracks)
	return(session,tracks,devices,clips)