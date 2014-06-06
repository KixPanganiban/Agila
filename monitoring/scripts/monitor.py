#!/usr/bin/env python
# Script to be executed to determine the uptime
# data 
# 
# @author ibaguio

import subprocess
from Usage import Usage, UsageManager

#http://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output
def getUptime():
    def runProcess(exe):    
        p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while(True):
          retcode = p.poll() #returns None while subprocess is running
          line = p.stdout.readline()
          yield line
          if(retcode is not None):
            break

    itm = None
    for line in runProcess('uptime'):
        if line: return line.strip()

def run():
    um = UsageManager()
    y = getUptime()
    um.update(Usage.create(y))
    um.sync()
    #save the created instance using cPickle

if __name__ == '__main__':
    run()