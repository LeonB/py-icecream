class Callback(object):
    """Can be anything: file, script, stdin, et cetera"""
    """It's meant to be extended, not used directly"""

    #@TODO: how should the input of ogg files be handled?
            #because they don't have to be de-coded

    def __init__(self):
        pass

    def run(self):
        #maybe call the childclass method different
        #and check here for correct output (http://, file://, et cetera)
        raise Exception('NIY', 'function run() is not yet implemented!')
