from threading import Event
from threading import Thread
import time

class ProgressWatcher(Thread):

    def __init__ (self, backend):
        Thread.__init__(self)
        self.backend = backend
        self.exit_event = Event()

    def exit(self):
        self.exit_event.set()
        self.join()

    def run(self):
        import gst
        while not self.exit_event.isSet():
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