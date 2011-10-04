##########################################################
##########################################################
# description: abstract class that represents a generic Symbol box
#
# autor: jeraman
# date: 13/04/2010
##########################################################
##########################################################

from box    import *
from socket import *



#number class itself
class Symbol (Box):
    rcv = ""
    
    #constructor
    def __init__(self, x, y, id=-1):
        self.value = "symbol"
        Box.__init__(self,x, y, id)

    def create(self):
        command = Box.canvas + "obj " + str(self.x) + " " + str(self.y) + " sym ; "
        Box.snd.send_pd(command)
        Box.create(self)
        command = "id " + str(search_box(self)+1) + " ; "
        #print command
        Box.snd.send_pd(command)
        sleep(0.1)
    
    @staticmethod
    def init_socket(r):
        Symbol.rcv = r
        
    #get the value from pd
    def get_value(self):
        #temp = Symbol.rcv.recv(32)
        #temp = temp[:(len(temp)-2)]
        #brk = temp.rfind("\n")
        
        #if brk == -1: #se nao encontrou
        #    self.value = temp
        #else:
        #    print brk
        #    self.value = temp[(brk+1):len(temp)] #se encontrou
        
        return self.value
        
    
    #edits this object
    def set(self, value): 
        #sets no-edit mode
        command  = Box.canvas + "editmode 1 ; "
        command += Box.canvas + "editmode 0 ; "
        Box.snd.send_pd(command)
        
        self.click() #clicks
        
        for i in self.value: #delete all previous keys
            command += Box.canvas + "key 1 8 0 ; " 
            command += Box.canvas + "key 0 8 0 ; "  
        for i in value: #sends all key pressed
            command += Box.canvas + "key 1 " + str(ord(i)) + " 0 ; " 
            command += Box.canvas + "key 0 " + str(ord(i)) + " 0 ; "   
        Box.snd.send_pd(command)
        command  = Box.canvas + "key 1 10 0 ;" # press enter
        command += Box.canvas + "key 0 10 0 ;"
        #self.value = self.get_value()
        command += Box.canvas + "editmode 1 ; "
        Box.snd.send_pd(command)
        
        self.value=value
    
    
    #aux static function to debug this class
    @staticmethod
    def debug():
        o = Symbol(10, 10, 0)
        print o.set("mesa")