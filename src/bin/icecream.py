#!/usr/bin/env python

import sys
sys.path.append('./')
sys.path.append('..i/')

# lines = sys.stdin.readlines()

# for line in lines:
#         sys.stdout.write(line)

#from server import Server
#import sources

#script = sources.Script()
#script.location = ''

#s = Server(source)
#s.password = 'hackmePbq11Kz'

import pyicecream
from pyicecream import sources
#from pyicecream.stream import Stream

#This should be wrapped in App, which should also do the configuration part
s = pyicecream.Stream()
s.server.host = 'basil'
s.server.password = 'hackmePbq11Kz'
s.source = sources.Disk('/home/leon/Workspaces/py-icecream/samples/gapples/flac')
s.run()
