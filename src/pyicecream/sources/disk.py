from pyicecream.source import Source
import os, glob
from humansort import *
import Queue

#@TODO: use inotify for watching the directory?

class Disk(Source):
    def __init__(self, path, random = False, repeat = True, recursive = True):
        super(Disk, self).__init__()
        self.path= path
        self.random = random
        self.repeat = repeat
        self.recursive = recursive
        self.queue = Queue.Queue()

        found_files = []
        for path in glob.glob(os.path.expanduser(self.path)):
            if os.path.isfile(path):
                found_files.append(path)

            if not self.recursive:
                for file in os.listdir(path):
                    if not os.path.isfile(file):
                        continue
                    found_files.append(path + os.sep + file)
            else:
                for root, dirs, files in os.walk(path):
                    for file in files:
                        found_files.append(root + os.sep + file)
        
        humansort(found_files)
        for file in found_files:
            self.queue.put(file)

    def get(self):
        return 'file://' + self.queue.get(False)
