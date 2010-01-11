import pyicecream
from progresswatcher import ProgressWatcher
import new
import tempfile
from silence import Silence

class Stream(object):
    name = 'py-icecream stream'
    description = None
    progress_watcher = None
    check_interval = 5
    interval_sound = None

    def __init__(self):
        self.server = pyicecream.Server()
        self.source = pyicecream.Source()
        self.backend = pyicecream.Backend(self)

        self.hooks = new.classobj('hooks', (object,), {})()

        self.hooks.source = pyicecream.HooksHolder()
        self.hooks.source.add_hook('start_play')
        self.hooks.source.add_hook('halfway')
        self.hooks.source.add_hook('transition')
        self.hooks.source.add_hook('eof')

        self.hooks.stream = pyicecream.HooksHolder()
        self.hooks.stream.add_hook('eos')
        self.hooks.stream.add_hook('stop')

        self.interval_sound = self.silent_file()

    def run(self):
        """This should read the source and start streaming"""
        self.backend.uri = self.source.get()

        if not self.backend.uri:
            raise IOError('No file given')

        self.backend.play()

        #Voortgang in de gaten houden:
        self.progress_watcher = ProgressWatcher(self.backend)
        self.progress_watcher.daemon = True
#        self.progress_watcher.start()

    def stop(self):
        self.hooks.stream.call('stop')
        self.progress_watcher.exit()

    def silent_file(self):
        self._tempfile = f = tempfile.NamedTemporaryFile()
        s = Silence()
        s.frequency = 0
        s.length = self.check_interval
        s.write(f.name)
        return f.name