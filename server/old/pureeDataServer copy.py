# Pure'eData Server by Ted Hayes & Sofy Yuditskaya 2010
# adapted from invaluable code by Jeraman
# http://jeraman.wordpress.com/2009/03/22/how-to-use-pure-data-as-a-api/

import sys
import os
import threading
import json
import subprocess as sub

from socket     import *
from time       import *
from subprocess import *

import web
import logging

#web.py vars
urls = ("/pd", "Pd",
        "/list", "List",
        '/', 'Index'
)

#app = web.application(urls, globals())
render = web.template.render('/var/www/PureeData/web')

#absolute path to server.pd
serverDir = "/var/www/PureeData/server"
#absolute path to pdsend
pdsendDir = "/usr/bin"
#the port used
port = 3005
pdReceivePort = 3006

#pd master objects list
objects = []
#objcount = 0

logging.basicConfig(filename='/var/www/PureeData/pureedata.log',level=logging.DEBUG)
logging.info("------------------START--------------------")

class Index:
    def GET(self):
        return render.index()

class PdObject:
    def __init__(self, type, content="", x=0, y=0, dontCreate=False):
        global objects
        #global objcount
        
        logging.info("Creating object: %s", content)
        
        self.id = len(objects)
        #self.x = objcount * 30
        #self.y = objcount * 30
        self.x = x
        self.y = y
        self.type = type
        self.content = content
        self.msg = "pd-new %s %d %d %s \;" % (type, x, y, content)
        
        objects.append(self)
        #objcount += 1
        if not dontCreate:
            sendPdMessage(self.msg)
        logging.info("... create done")
        
    def getObj(self):
        print "getObj"
        return {
            'id'        :self.id,
            'x'         :self.x,
            'y'         :self.y,
            'type'      :self.type,
            'content'   :self.content,
            'msg'       :self.msg
        }
        
def connectObjects():
    msg = "pd-new connect %d %d %d %d \;" % (obj1, let1, obj2, let2)

def sendPdMessage(msg):
    logging.debug("--> sending message: %s", msg)
    os.system("cd %s && echo %s | ./pdsend %d" %(pdsendDir, msg, port))

def makeJSON(data):
    tempData = []
    for o in data:
        print o
        tempData.append(o.getObj())
    
    output = json.dumps(tempData, indent=4)               
    web.header("Content-Type", "text/plain")
    #print json.dumps(tempData)
    logging.debug("makeJSON: %s", tempData)
    return output

class Pd:
    def POST(self):
        global objects
        i = web.input()
        logging.debug("Pd.POST: %s", i)
        if hasattr(i, "obj"):
            theobj = PdObject("obj", i.obj)
            #print "obj: "+theobj.getObj
            return makeJSON([theobj])

        if hasattr(i, "msg"):
            theobj = PdObject("msg", i.msg)
            return makeJSON([theobj])
        
        if hasattr(i, "dsp"):
            val = str(i.dsp)
            sendPdMessage("pd dsp "+val+" \;")
            return "success"
            
        if hasattr(i, "clear"):
            objects = []
            sendPdMessage("pd-new clear \;")
            return "success"
            
        if hasattr(i, "connect"):
            logging.debug("Connecting...")
            return "success"
        
        if hasattr(i, "update"):
            # update an object
            logging.debug("Updating object...")
            return "success"
        
        return "Error: No recognized commands"

class List:
    def GET(self):
        #global objects
        return makeJSON(objects)

class PdReceiveThread( threading.Thread ):
    def run(self):
        p2 = Popen("%s/pdreceive %d"%(pdsendDir, pdReceivePort),shell=True, stdout=sub.PIPE,stderr=sub.PIPE)
        go = 1
        while go:
            p2read = p2.stdout.readline().rstrip(";\n")
            #print "got "+p2read
            if p2read == "test":
                print "GOT TEST"
            elif p2read == "stop":
                print "STOPPING PdReceiveThread"
                p2.kill()
                go = 0
            elif "=" in p2read:
                key, eq, val = p2read.partition("=")
                if key == "val":
                    print "val is "+val

# a thread class that we're gonna use for calling the server.pd patch
class PdThread ( threading.Thread ):
   def run ( self ):
       temp = "cd %s && ./pdextended -nogui %s/server.pd" %(pdsendDir, serverDir)
       p = Popen(temp, shell=True)

#if __name__ == "__main__":
    #print "Initializing PureData..."
    #PdThread().start()
    #sleep(40)
    #print "Starting pdreceive..."
    #PdReceiveThread().start()
    #print "Starting web.py server..."
    #app.run()

logging.info("Making send~ objects")
# type, content="", x=0, y=0, dontCreate=False
lsend = PdObject("obj", "send~ left", x=300, y=400, dontCreate=True)
rsend = PdObject("obj", "send~ right", x=400, y=400, dontCreate=True)

logging.info("Starting web.py server")
application = web.application(urls, globals()).wsgifunc()