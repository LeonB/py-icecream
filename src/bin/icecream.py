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

import pyicecream
from pyicecream import sources
from pyicecream import callbacks

#This should be wrapped in App, which should also do the configuration part
s = pyicecream.Stream()
s.server.host = 'basil'
s.server.port = 9000
s.server.password = 'hackmePbq11Kz'
#s.source = sources.Disk('~/Music/02 Paranoid Android.mp3')
#s.source = sources.Disk('~/Workspaces/py-icecream/samples/gapless')
#s.source = sources.Disk('~/Workspaces/py-icecream/samples/gapless/*/*.ogg')
#s.source = sources.Disk('~/Workspaces/py-icecream/samples/gapless/*/*.flac')
#s.source = sources.Disk('~/Workspaces/py-icecream/samples/gapless/ogg/16. Beethoven.ogg')
#s.source = sources.Script('~/Workspaces/py-icecream/src/test/scripttest.py')
#s.source = sources.Script('wget -qO- http://basil/playlist | cat')
s.source = sources.Script('wget -qO- http://localhost:3000/playlists/default.xml |perl -ne \'if (?(<location>(.*)<\/location>)?) {print "file:\/\/$2\n"}\'')

s.hooks.source.transition.add_callback(callbacks.Script("echo 'Dit is een overgang!'").run)
s.hooks.stream.eos.add_callback(callbacks.Script("echo 'Dit is het einde van alles....'").run)
s.hooks.source.start_play.add_callback(callbacks.Script("echo 'Start van een nieuw liedje'").run)
s.hooks.source.halfway.add_callback(callbacks.Script("echo 'Jeuh, halverwege het liedje!'").run)

# enter into a mainloop
loop = gobject.MainLoop()

s.hooks.stream.eos = loop.quit

s.run()
loop.run()

print 'aaargghhh'
s.source = sources.Disk('~/Music/02 Paranoid Android.mp3')
s.run()
loop.run()

print 'ookokoko'