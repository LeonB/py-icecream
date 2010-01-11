from pyicecream.callback import Callback
import subprocess
import string

class Script(Callback):

    def __init__(self, command):
        self.command = command

    def run(self, *args):
        bash_arguments = []
        for arg in args:
           bash_arguments.append("'" + arg.replace("'", "'\\''") + "'")

        command_with_arguments = self.command + ' ' + string.join(map(str, bash_arguments), ' ')

        #maybe give arguments such as previous output et cetera
        sp = subprocess.Popen(command_with_arguments, shell=True, stdout=subprocess.PIPE)
        output = sp.communicate()[0]

        if sp.returncode > 0:
            'something went wrong'
        else:
            print output
            return output
