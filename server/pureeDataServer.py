# Pure'eData Server by Ted Hayes & Sofy Yuditskaya 2010
# adapted from code by Jeraman
# http://jeraman.wordpress.com/2009/03/22/how-to-use-pure-data-as-a-api/

import sys
import os
import threading

from socket     import *
from time       import *  
from subprocess import *

import web

urls = ("/pd", "Pd")
        
app = web.application(urls, globals())

class Pd:
    def POST(self):
        i = web.input()
        # return i.obj
        if i.obj != "":
            theobj = i.obj
            msg = "pd-new obj %d %d %s \;" % (x, y, theobj)
            print "* obj: %s"%(msg)
            os.system("cd %s && echo %s | ./pdsend %d" %(pdsendDir, msg, port))
            print "--> Sent."
            return theobj
        else: return "nothin'"
        
    def GET(self):
        return 'hello, Pd!'

#some variables
x = 10
y = 0

#pd objects list
objects = []

#absolute path to server.pd
serverDir = "//Users/daleth/Projects/PureeData/pureeData/server"
#absolute path to pdsend
pdsendDir = "//Applications/Pd-extended.app/Contents/Resources/bin"
#the port used
port = 3005

# a thread class that we're gonna use for calling the server.pd patch
class PdThread ( threading.Thread ):
   def run ( self ):
       temp = "cd %s && ./pd -nogui %s/server.pd" %(pdsendDir, serverDir)
       p = Popen(temp, shell=True)

if __name__ == "__main__":    
    #print "Initializing PureData..."
    #PdThread().start()
    #sleep(40)
    print "Starting web.py server..."
    app.run()