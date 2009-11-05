import pyicecream

class Stream(object):

    def __init__(self):
        self.server = pyicecream.Server()
        self.source = pyicecream.Source()
        self.backend = pyicecream.Backend(self)

    def run(self):
        """This should read the source and start streaming"""
        self.backend.uri = self.source.get()
        self.backend.play()
        #self.source.pop() #must be called from backend
