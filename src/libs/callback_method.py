import callbacks

def callback_method(what, *args):
    def with_callback_method(self):
        methodname = what.__name__
        callbacks.RunAllCallbacks(self.__class__, 'before_' + methodname, self)
        result = what(self)
        callbacks.RunAllCallbacks(self.__class__, 'after_' + methodname, self)
        return result
    return with_callback_method