import pyicecream
import sys

class Server(object):
    name = ''
    description = ''
    genre = ''
    
    host = 'localhost'
    port = 8000
    user = 'source'
    password = 'hackme'
    mount = sys.argv[0]
    
    format = None
    protocol = None

    #def __init__(self, source):
        ##build in a check
        #self.source = source
