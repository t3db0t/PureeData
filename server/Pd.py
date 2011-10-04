

##########################################################
##########################################################
# description: main class that emulates Pd
#
# autor: jeraman
# date: 16/04/2010
##########################################################
##########################################################



from basic_classes.box import *
from basic_classes.object import *
from basic_classes.message import *
from basic_classes.number import *
from basic_classes.symbol import *
from basic_classes.comment import *
from basic_classes.connection import *
from communication import *
from gui_updater import *   
from transfer_board import * 



class Pd():
    #construtor
    def __init__(self):
        self.c = Communication(True)
        self.b = ""
        self.tb = TransferBoard()
    
    #inicializando a api
    def init(self, usePdThread=True):
        self.c.init_pd(usePdThread)
        self.clear()
        self.dsp(True)
        self.editmode(True)
        
        self.b = GuiUpdater(self.c.rcv)
        self.b.start()
        
    #finalizando a api
    def quit(self):
        self.clear()
        self.save()
        self.dsp(False)
        GuiUpdater.finish = True
        self.c.finish_pd()

        
    #salvando o arquivo
    def save(self):
        print "Pd: Saving patch"
        self.c.save_state(Box.canvas)
        
    #cleans the patch
    def clear(self):
        print "Pd: Clearing Patch"
        self.c.send_pd(Box.canvas + "clear ; ")
        del memory_box[:]  
        del memory_connections[:]  
        
        
    
    #modifies the editmode. receives a boolean.
    def editmode(self, on_off):
        command = Box.canvas + "editmode 1 ; "
        if on_off==False:
            command += Box.canvas + "editmode 0 ; "
        self.c.send_pd(command)
    
    #modifies the dsp. receives a boolean
    def dsp(self, on_off):
        if on_off==False:
            self.c.send_pd("; pd dsp 0 ; ")
        else:
            self.c.send_pd("; pd dsp 1 ; ")
   
   #returns the memory available in Pd     
    def get_box_list(self):
        return memory_box
    
    #return the connections available in Pd
    def get_connection_list(self):
        return memory_connections
    
    
    
    #################################
    ## EDIT MENU METHODS
    #################################

    #copy method
    def copy(self):
        self.tb.copy()
    
    #paste method
    def paste(self, x, y):
        self.tb.paste(x, y)
        
    #cut method
    def cut(self):
        self.tb.cut()
        
    #duplicate method
    def duplicate(self, x, y):
        self.tb.duplicate(x, y)
              
    #select all method
    def selectall(self):
        command = Box.canvas + "selectall ; "
        self.c.send_pd(command)
        self.tb.selectall()
    
    
    
    #################################
    ## FIND MENU METHODS
    #################################
    
    #finds a given box by its label
    def find(self, label):
        command = self.canvas + "find " + str(label) + " ; "
        self.send.send_pd(command)
    
    #continues the last find called
    def findagain(self):
        command = self.canvas + "findagain ; "
        self.send.send_pd(command)
    
    def finderror(self):
        command = "; pd finderror"
        self.send.send_pd(command)
    
    