from subprocess import Popen, PIPE

class Cmd(object):
    def __init__(self, cmd):
        self.cmd = cmd
    def __call__(self, *args):
        command = '%s %s' % (self.cmd, ' '.join(args))
        result = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)

class Sh(object):
    def __getattr__(self, attribute):
        return Cmd(attribute)