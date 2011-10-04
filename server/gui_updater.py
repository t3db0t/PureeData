

##########################################################
##########################################################
# description: class that get all values from GUI boxes inside Pd, updating python values
#
# autor: jeraman
# date: 21/04/2010
##########################################################
##########################################################

from threading  import *
from basic_classes.box import *

class GuiUpdater(Thread):
    #class variable that indicates if the thread should end
    finish = False
    
    #constructor  
    def __init__(self, rcv):
        Thread.__init__(self)
        self.rcv = rcv
        
    #run method
    def run(self):
        while not(GuiUpdater.finish):
            temp = self.rcv.recv(1024)
            commands = temp.split(";")
            
            for c in commands:
                i = c.rfind(" ")
                #print c
                #verifica se a string nao veio quebrada
                result = c.split(" ")
                if len(result) > 1:                
                    value = c[0:i]
                    id= int(c[i:len(c)])
                    box=memory_box[id-1] #get the box
                    box.value=value #updates its value   