import callbacks
from callbacksholder import CallbacksHolder

class HooksHolder(object):

    def call(self, hook, *args):
        callbacks.RunCallbackChain(self, hook, *args)

    def add_hook(self, hook):
         setattr(self, hook, CallbacksHolder(self, hook))