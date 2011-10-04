

##########################################################
##########################################################
# description: class that aux the copy/paste/duplicate/etc stuff
#
# autor: jeraman
# date: 22/04/2010
##########################################################
##########################################################


from basic_classes.box import *
import copy

class TransferBoard():
    def __init__(self):
        self.memory = []
    
    #copy method
    def copy(self):
        del self.memory[:]
        for b in memory_box:
            if b.selected:
                self.memory.append(copy.deepcopy(b))
            
    #paste method
    def paste(self, x, y):
       for b in self.memory:
           b.x+=x
           b.y+=y           
           b.create()
        
    #cut method
    def cut(self):
        self.copy()
        for b in memory_box:
            if b.selected:
                b.delete()
        
    #duplicate method
    def duplicate(self, x, y):
        self.copy()
        self.paste(x, y)
        
    #select all method
    def selectall(self):
        for b in memory_box:
            b.shift_select()
    