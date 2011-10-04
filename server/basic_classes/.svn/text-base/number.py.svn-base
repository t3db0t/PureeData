
##########################################################
##########################################################
# description: abstract class that represents a generic Number box
#
# autor: jeraman
# date: 13/04/2010
##########################################################
##########################################################

from box    import *
from socket import *
from time import *



#number class itself
class Number (Box):
    #class variables
    rcv = ""
    
    #constructor
    def __init__(self, x, y, id =-1):
        self.value = 0
        Box.__init__(self,x, y, id)        

    def create(self):
        command = Box.canvas + "obj " + str(self.x) + " " + str(self.y) + " nmb ; "
        Box.snd.send_pd(command)
        Box.create(self)
        command = "id " + str(search_box(self)+1) + " ; "
        #print command
        Box.snd.send_pd(command)
        sleep(0.1)
    
    @staticmethod
    def init_socket(r):
        Number.rcv = r
        
    #get the value from pd
    def get_value(self):
        sleep(0.1)
        return int(self.value)
        
    
    #edits this object
    def set(self, value): 
        #sets no-edit mode
        command  = Box.canvas + "editmode 1 ; "
        command += Box.canvas + "editmode 0 ; "
        Box.snd.send_pd(command)
        
        self.click() #clicks
        
        #str_value = str(self.value) # transforms the value to str
        #for i in str_value: #delete all previous keys
        #    command += Box.canvas + "key 1 8 0 ; " 
        #    command += Box.canvas + "key 0 8 0 ; " 
        #Box.snd.send_pd(command)
        
        str_value = str(value) # transforms the value to str
        for i in str_value: #sends all key pressed
            command += Box.canvas + "key 1 " + str(ord(i)) + " 0 ; "
            command += Box.canvas + "key 0 " + str(ord(i)) + " 0 ; "   
        Box.snd.send_pd(command)
        
        command  = Box.canvas + "key 1 10 0 ; " # press enter
        command += Box.canvas + "key 0 10 0 ; "
        
        #sets edit mode
        command += Box.canvas + "editmode 1 ; "
        
        Box.snd.send_pd(command)
    
    #increments the lowest amount from the value of a number
    def increment(self):
        #sets no-edit mode
        command  = Box.canvas + "editmode 1 ; "
        command += Box.canvas + "editmode 0 ; "
        Box.snd.send_pd(command)
        
        command  = Box.canvas + "mouse " + str(self.x+1) + " " + str(self.y+1) + " 1 0 ; "
        command += Box.canvas + "motion " + str(self.x+1) + " " + str(self.y) + " 0 ; "
        command += Box.canvas + "mouseup " + str(self.x+1) + " " + str(self.y) + " 1 0 ; "
        #self.value = self.get_value()
        
        command += Box.canvas + "editmode 1 ; "
        Box.snd.send_pd(command)
    
    #decrements the lowest amount from the value of a numbe
    def decrement(self):
        #sets no-edit mode
        command  = Box.canvas + "editmode 1 ; "
        command += Box.canvas + "editmode 0 ; "
        Box.snd.send_pd(command)
        
        command  = Box.canvas + "mouse " + str(self.x+1) + " " + str(self.y+1) + " 1 0 ; "
        command += Box.canvas + "motion " + str(self.x+1) + " " + str(self.y+2) + " 0 ; "
        command += Box.canvas + "mouseup " + str(self.x+1) + " " + str(self.y+2) + " 1 0 ; "
        #self.value = self.get_value()
        command += Box.canvas + "editmode 1 ; "
        Box.snd.send_pd(command)
    

    
    
    #aux static function to debug this class
    @staticmethod
    def debug():
        o = Number(10, 10, 0)
        print o.set(20)
        print o.increment()
        print o.decrement()    