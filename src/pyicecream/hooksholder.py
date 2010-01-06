class HooksHolder(object):
    def call(self, attr_name, *args):
        if not hasattr(self, attr_name):
            return False

        attr = getattr(self, attr_name)

        if callable(attr):
            return attr(*args)

        if not hasattr(attr, 'run'):
            return False

        run_attr = getattr(attr, 'run')

        if callable(run_attr):
            return run_attr(*args)

        return False

        
            