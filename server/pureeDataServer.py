# Pure'eData Server by Ted Hayes & Sofy Yuditskaya 2010
# adapted from invaluable code by Jeraman
# http://jeraman.wordpress.com/2009/03/22/how-to-use-pure-data-as-a-api/

import sys
import os
# make sure this script can find the Pd classes
cmd_folder = os.path.dirname(os.path.abspath(__file__))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
import threading
import json
import subprocess as sub
import web
import logging
from socket     import *
from time       import *
from subprocess import *
from Pd         import *

#web.py vars
urls = ("/pd", "PdCommand",
        "/list", "List",
        '/', 'Index'
)

#app = web.application(urls, globals())
render = web.template.render('templates')

#absolute path to server.pd
serverDir = "/var/www/PureeData/server"
# this stuff in properties.config
#absolute path to pdsend
#pdsendDir = "/usr/bin"
#the port used
#port = 3005
#pdReceivePort = 3006

#pd master objects list
allObjects = []
pd = None     # declare as global (?)

# redirect print statements to logfile
class LogStream(object):
    def write(self, data):
        logging.debug(data)
sys.stdout = LogStream()

logging.basicConfig(filename='/var/www/PureeData/pureedata.log',level=logging.DEBUG, format='[%(asctime)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.info("------------------START--------------------")

class Index:
    def GET(self):
        return render.index()

def getObjProps(pdObj):
    if hasattr(pdObj, 'label'):
        content = pdObj.label
        type = 'obj'
    elif hasattr(pdObj, 'text'):
        content = pdObj.text
        type = 'msg'
    else:
        content = '';
    
    return {
        'id'        : pdObj.id,
        'x'         : pdObj.x,
        'y'         : pdObj.y,
        'type'      : type,
        'content'   : content
    }

def makeJSON(data):
    tempData = []
    logging.debug("makeJSON: data: %s", data)
    for o in data:
        tempData.append(getObjProps(o))
    
    output = json.dumps(tempData, indent=4)
    web.header("Content-Type", "text/plain")
    logging.debug("makeJSON: %s", tempData)
    return output

class PdCommand:
    def POST(self):
        global allObjects
        i = web.input()
        logging.debug("Pd.POST: %s", i)
        if hasattr(i, 'cmd'):
            if i.cmd == 'obj':
                logging.debug("Making object: %s" % i.obj)
                try:
                    theobj = pdObject(int(i.x), int(i.y), i.obj)
                    logging.debug("inlets: %s / outlets: %s", theobj.inlets, theobj.outlets)
                except error, e:
                    return "error: %s" % e
                return makeJSON([theobj])
            
            if i.cmd == "msg":
                try:
                    theobj = pdMessage(int(i.x), int(i.y), i.msg)
                except error, e:
                    return "error: %s" % e
                return makeJSON([theobj])
            
            if i.cmd == "msgclick":
                result = memory_box[int(i.id)].click()
                #logging.debug('msgclick result: %s',result)
                return result
            
            if i.cmd == "dsp":
                val = int(i.dsp)
                try:
                    if(val == 1):
                        pd.dsp(True)
                    if(val == 0):
                        pd.dsp(False)
                except error, e:
                    return "error: %s" % e
                return "success"
            
            if i.cmd == "savePatch":
                logging.debug("Saving patch...")
                #allObjects = []
                try:
                    pd.save()
                    # remove all but lsend and rsend
                except error, e:
                    return "error: %s" % e
                return "success"
            
            if i.cmd == "clear":
                logging.debug("Clearing patch...")
                try:
                    #pd.clear()
                    # remove all but lsend and rsend
                    pass
                except error, e:
                    return "error: %s" % e
                return "success"
                
            if i.cmd == "connect":
                #logging.debug("Connecting... [%s: %s] to [%s: %s]", i.firstID, i.outlet, i.secondID, i.inlet)
                status = connect(memory_box[int(i.firstID)], i.outlet, memory_box[int(i.secondID)], i.inlet)
                if status:
                    # return connection object
                    c = getConnectionProps(memory_connections[len(memory_connections)-1])
                    #logging.debug('c: %s', c)
                    return json.dumps(c)
                else:
                    logging.error('*** Connection error')
                    return web.internalerror("Connection error")
            
            if i.cmd == "disconnect":
                try:
                    c = memory_connections[int(i.id)]
                    c.delete()
                except error, e:
                    return "error: %s" % e
                output = {
                    'id':int(i.id)
                }
                return json.dumps(output)
            
            if i.cmd == "update":
                # update an object
                logging.debug("Updating object...")
                return "success"
            
            if i.cmd == "move":
                logging.debug("Moving object...")
                obj = memory_box[int(i.id)]
                obj.move(int(i.x), int(i.y))
                return "success"
            
            if i.cmd == "delObject":
                logging.debug("Deleting object %s", i.id)
                obj = memory_box[int(i.id)]
                obj.delete()
                return "success"
            
            if i.cmd == "quit":
                pd.quit()
                return "success"
        
        return "Error: No recognized commands"

class List:
    def GET(self):
        objs = getAllObjects()
        conns = getAllConnections()
        tempData = {
            'objects': objs,
            'connections': conns
        }
        return json.dumps(tempData, indent=4)

def getAllConnections():
    #parse through all connection objects and format relevant information
    tempData = []
    for c in memory_connections:
        conn = getConnectionProps(c)
        tempData.append(conn)
    return tempData

def getAllObjects():
    tempData = []
    for o in memory_box:
        tempData.append(getObjProps(o))
    return tempData

def getConnectionProps(c):
    return {
        'id'        : c.id,
        'firstID'   : c.box_orig.id,
        'outlet'    : c.outlet,
        'secondID'  : c.box_dest.id,
        'inlet'     : c.inlet
    }

def pdObject(x, y, msg):
    global allObjects
    theObject = Object(x, y, msg, len(memory_box))
    allObjects.append(theObject)
    return theObject

def pdMessage(x, y, msg):
    global allObjects
    theObject = Message(x, y, msg, len(memory_box))
    allObjects.append(theObject)
    return theObject

if __name__ == "__main__":
    global pd
    #global allObjects
    #allObjects = []
    logging.info("Starting Pyata...")
    pd = Pd()
    pd.init(usePdThread=True)
    # TODO: may want to be able to keep the content of the patch between restarts?
    pd.clear()

    logging.info("Making send~ objects")
    lsend = pdObject(300, 400, "send~ left")
    rsend = pdObject(400, 400, "send~ right")
    
    logging.info("Starting web.py server")
    #application = web.application(urls, globals()).wsgifunc()
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()