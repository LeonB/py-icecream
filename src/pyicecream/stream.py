import pyicecream

class Stream(object):

    def __init__(self):
        self.server = pyicecream.Server()
        self.source = pyicecream.Source()

    def run(self):
        """This should read the source and start streaming"""
        pass
