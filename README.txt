[code]
from py-icecream import Server
import gobject

s = Server()
s.password = "hackmePbq11Kz"

#En nu.....
s.queue().add('/home/leon/Workspaces/pmpd/samples/flac/*.flac')

#start playing/sending the data
s.start()

# enter into a mainloop
loop = gobject.MainLoop()
loop.run()
[/code]

Or maybe:

[code]
from py-icecream import Server
import gobject

s = Server()
s.password = "hackmePbq11Kz"

#En nu.....
#@TODO: iets toevoegen met een callback zodat mogelijk is om de volgende 
# file toe te voegen

f = open('/home/leon/Workspaces/pmpd/samples/flac/*.flac')
nbuf = f.read(4096)
while 1:
    buf = nbuf
    nbuf = f.read(4096)
    total = total + len(buf)
    if len(buf) == 0:
        break
    s.send(buf)
    s.sync()
f.close()


# enter into a mainloop
loop = gobject.MainLoop()
loop.run()
[/code]
