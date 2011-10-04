##########################################################
##########################################################
# description: class that handles pd communication
#
# important: based on Frank Barknecht script at:
# http://markmail.org/message/ohuwrz77hwo3bcwp#query:python%20pdsend+page:1+mid:ybdc6esbu7q53otu+state:results 
#
# autor: jeraman
# date: 06/04/2009
##########################################################
##########################################################

#import sys
from threading  import *
from socket     import *
from time       import *  
from subprocess import *
from basic_classes.box import *
from basic_classes.number import *
from basic_classes.symbol import *
from basic_classes.connection import *






# a thread class that we're gonna use for calling the server.pd patch
class RemotePd ( Thread ):
    def __init__(self, nogui, pd_dir, server_dir):
       Thread.__init__(self)
       self.nogui = nogui
       self.server_dir = server_dir
       self.pd_dir = pd_dir
       
   #run method 
    def run ( self ):
       if self.nogui:
           temp = "cd %s && pdextended -nogui %s/server.pd" %(self.pd_dir, self.server_dir)
       else:
           temp = "cd %s && pdextended %s/server.pd" %(self.pd_dir, self.server_dir)
       self.p = Popen(temp, shell=True)




#communication class
class Communication(): 
    
    #constructor
    def __init__(self, nogui): 
        # variables from config file
        self.pd_dir = ""
        self.server_dir = "/var/www/PureeData/server/aux_patches"
        self.host = "localhost" 
        #self.snd_port = "" 
        #self.rcv_port = ""      
        #self.load_config() #loads the properties.config
        self.pd_dir = "/usr/bin"
        self.rcv_port = 3001
        self.snd_port = 3000

        #class variables
        self.snd_socket = socket(AF_INET, SOCK_STREAM)
        self.rcv_socket = socket(AF_INET, SOCK_STREAM)
        self.thread=RemotePd(nogui, self.pd_dir, self.server_dir)
        self.file = open(self.server_dir+"/server.pd","r")
        #self.rcv = ""

    #loads the properties.config
    def load_config(self):
        #config = open("/var/www/PureeData/server/properties.config","r")

        #reads the pd dir
        temp = config.readline()
        while(temp[0]=="#"):
            temp = config.readline()
        self.pd_dir = temp[:len(temp)-1]

        #reads the server dir
        temp = config.readline()
        while(temp[0]=="#"):
            temp = config.readline()
        self.rcv_port = int(temp)

        #reads the server dir
        temp = config.readline()
        while(temp[0]=="#"):
            temp = config.readline()
        self.snd_port = int(temp)

        config.close()
        
    #connecting to pd
    def init_pd(self, usePdThread=True): 
        if(usePdThread):
            print "Initializing server.pd in seperate thread..."
            self.thread.start()
            sleep(5)
        else:
            print "Trying to connect to existing Pd instance..."
        
        try: 
            print "Connecting to Send Port: %s" % self.snd_port
            self.snd_socket.connect((self.host, self.snd_port))
            print "Binding to Receive Port: %s" % self.rcv_port
            self.rcv_socket.bind((self.host, self.rcv_port))
            self.rcv_socket.listen(1) 
            self.rcv, addr = self.rcv_socket.accept()
            self.init_pyata()
            print "Connected with Pd"
            return True
        except error, err: 
            print "Error connecting to %s:%d: %s" % (self.host, self.snd_port, err) 
            return False
    
    #init some socket variables
    def init_pyata(self):
        Box.set_sender(self)
        Connection.set_sender(self)
        Number.init_socket(self.rcv)
        Symbol.init_socket(self.rcv)
    
    
    #sending a command to pd
    def send_pd(self, commands):
        try:
            self.snd_socket.send(commands)
            return True
        except error, err: 
            print "Error sending message %s : %s" % (commands, err) 
            return False


    #closing connection
    def finish_pd(self): 
        try: 
            temp = "killall pd"
            p = Popen(temp, shell=True)
            
            self.snd_socket.close() 
            self.rcv_socket.close()
            self.file.close()
            print "closing connection with pd" 
            return True
        except error, err: 
            print "Error sending message %s : %s" % (message, err) 
            return False   

    
    def save_state(self, canvas):
        self.snd_socket.send(canvas + "menusave ; ")
        sleep(0.1)
    
    #returns the useful content of a file
    def get_file(self):
        self.file.seek(0)
        text = self.file.read()
        i = text.find("new")
        text = text[(i+7):(len(text))]
        i = text.find("pd new;")
        text = text[0:(i-18)]
        
        return text
        
    #setting the canvas to where the messages are going
    def set_canvas(self, canvas):
        self.canvas=canvas
        
    #aux static function to debug this class
    @staticmethod
    def debug():
        c = Communication(False)
        c.init_pd()
        sleep(5)
        c.finish_pd()
        
        

        