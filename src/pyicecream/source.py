class Source(object):
    """Can be anything: file, script, stdin, et cetera"""
    """It's meant to be extended, not used directly"""

    #@TODO: how should the input of ogg files be handled?
            #because they don't have to be de-coded

    def __init__(self):
        pass

    def get(self):
        #maybe call the childclass method different
        #and check here for correct output (http://, file://, et cetera)
        raise Exception('NIY', 'function get() is not yet implemented!')
