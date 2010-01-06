import pyicecream
import new

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
        #self.source.pop() #must be called from backend
