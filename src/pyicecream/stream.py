import threading
import pyicecream
import new
#from threading import Thread
from multiprocessing import Process
import time
import sys

class Stream(object):

    def __init__(self):
        self.server = pyicecream.Server()
        self.source = pyicecream.Source()
        self.backend = pyicecream.Backend(self)

        self.hooks = new.classobj('hooks', (object,), {})()

        self.hooks.source = pyicecream.HooksHolder()
        self.hooks.source.start_play = lambda *args: None
        self.hooks.source.halfway = lambda *args: None
        self.hooks.source.transition = lambda *args: None
        self.hooks.source.eof = lambda *args: None

        self.hooks.stream = pyicecream.HooksHolder()
        self.hooks.stream.eos = lambda *args: None

    def run(self):
        """This should read the source and start streaming"""
        self.backend.uri = self.source.get()

        if not self.backend.uri:
            raise IOError('No file given')

        self.backend.play()

        #Voortgang in de gaten houden:
#        p = Process(target=self.watch_progress, args=(self))
#        p.start()
        
        t = threading.Thread(None, self.watch_progress)
        t.daemon = True
        t.start()

    def watch_progress(self):
        import gst
        while 1:
            try:
                pass
                pos = self.backend.query_position()
                dur = self.backend.query_duration()
                print pos
                print dur
                print float(pos)/float(dur)
                print '------------------------'
            except gst.QueryError, e:
                print e
            time.sleep(1)
