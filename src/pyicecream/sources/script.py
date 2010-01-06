from pyicecream.source import Source
import subprocess

class Script(Source):

    def __init__(self, path):
        self.path = path

    def get(self):
        #maybe give arguments such as previous output et cetera
        sp = subprocess.Popen(self.path, shell=True, stdout=subprocess.PIPE)
        output = sp.communicate()[0]

        if sp.returncode > 0:
            raise Exception('Error in script source', 'Something went wrong')
        else:
            file = output.split("\n")[0]

            if not file:
                raise Exception('InputError', 'Script "' + self.path + '" gave no output')

            return file
