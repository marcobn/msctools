#!/usr/bin/python

import setuptools
from distutils.core import setup
import os,sys
from os import path

setup(name='msctools',
	version='0.0',
	description='my collection of composing and performing tools in python',
	author='Marco Buongiorno Nardelli',
	author_email='mbn@unt.edu',
	platforms='OS independent',
	url='https://www.musicntwrk.com',
	packages=['msctools'],
	package_dir={'msctools':'./'},
	install_requires=['numpy','scipy','networkx','music21','librosa','pyo'],
)
