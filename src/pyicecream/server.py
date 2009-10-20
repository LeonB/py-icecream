import pyicecream

class Server(object):
    name = ''
    description = ''
    genre = ''
    
    host = 'localhost'
    port = 8000
    user = 'source'
    password = 'hackme'
    mount = ''
    
    format = None
    protocol = None

    source = pyicecream.Source()

    #def __init__(self, source):
        ##build in a check
        #self.source = source
