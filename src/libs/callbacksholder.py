from callbacks import RegisterCallback, PermanentCallback

class CallbacksHolder(object):
    hook = ''

    def __init__(self, scope, hook):
        self.scope = scope
        self.hook = hook

    def add_callback(self, callback, *args):
        RegisterCallback(self.scope, self.hook, PermanentCallback(callback))
