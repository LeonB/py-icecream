#!/usr/bin/env python


### Twisted Preamble
# This makes sure that users don't have to set up their environment
# specially in order to run these programs from bin/.
import sys
import os
bin_dir = os.path.dirname(os.path.realpath(__file__ ))
sys.path.append(bin_dir + os.sep + os.pardir + os.sep)
sys.path.append(bin_dir + os.sep + os.pardir + os.sep + 'libs' + os.sep)
### end of preamble

import gobject
gobject.threads_init()

# lines = sys.stdin.readlines()

# for line in lines:
#         sys.stdout.write(line)

#from server import Server
#import sources

#script = sources.Script()
#script.location = ''

#s = Server(source)
#s.password = 'hackme'

import pyicecream
from pyicecream import sources
#from pyicecream.stream import Stream

#This should be wrapped in App, which should also do the configuration part
s = pyicecream.Stream()
s.server.host = 'basil'
s.server.password = 'hackmePbq11Kz'
s.source = sources.Disk('~/Workspaces/py-icecream/samples/gapless')
s.source = sources.Script('~/Workspaces/py-icecream/src/test/scripttest.py')
s.run()

# enter into a mainloop
loop = gobject.MainLoop()
loop.run()
