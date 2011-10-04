
##########################################################
##########################################################
# description: abstract class that represents any Pd box
#
# autor: jeraman
# date: 13/04/2010
##########################################################
##########################################################

from time import *

memory_box = [] #stores all objetcs that are inserted to pd

def search_box (b):
    i=0
    #seraching for a specific box in memory
    for box in memory_box:
        if b==box:
            return i
        i+=1
    
    #return -1 if not
    if i==len(memory_box):
        return -1
    else:
        return i
   

         

#box class itself
class Box:
    # class variables (not instance variables
    canvas = "pd-new " #stores the name of the canvas
    snd = "" #used to communicate to pd
   
    #constructor of the class
    def __init__(self, x, y, id):
        self.x=x
        self.y=y
        self.id=id
        self.create()
        self.inlets = 0
        self.outlets = 0
        self.selected = False
        #self.inlet= self.verify_inlets()
        #self.outlet=self.verify_outlets()
    
    def create(self):
        #the rest of the code is defined in the subclasses
        self.selected = False
        memory_box.append(self) 
    
    def delete(self):
        self.select()
        command = Box.canvas + "cut ; "
        Box.snd.send_pd(command)
        
        i=search_box(self)
        
        if (i != -1):
            r = memory_box.pop(i)
        
            #ajustando os ids dos gui restantes apos remover um elemento
            #command = ""
            #print "i " + str(i)
            for id in range(i, len(memory_box)):
                command = "decrement " + str(id+2) + " ; "
                #print command
                Box.snd.send_pd(command); 
                sleep(0.01)
 
            return True
                
        else:
            print False
        

    #method that sets the canvas
    @staticmethod
    def set_canvas(nc):
        Box.canvas = nc
        
    #method that sets the sender
    @staticmethod
    def set_sender(s):
        Box.snd = s
    
    #clicks inside this obj
    def click(self):
        #command  = []
        command  = Box.canvas + "mouse " + str(self.x+1) + " " + str(self.y+1) + " 1 0 ; "
        command += Box.canvas + "mouseup " + str(self.x+1) + " " + str(self.y+1) + " 1 0 ; "
        Box.snd.send_pd(command)
        
    # method that moves this box   
    def move (self, new_x, new_y):
        command  = Box.canvas + "mouse " + str(self.x+1) + " " + str(self.y+1) + " 1 0 ; "
        command += Box.canvas + "motion " + str(new_x+1) + " " + str(new_y+1) + " 0 ; "
        command += Box.canvas + "mouseup " + str(new_x+1) + " " + str(new_y+1) + " 1 0 ; "
        self.x=new_x
        self.y=new_y
        Box.snd.send_pd(command)
        self.unselect()
    
    #method that selects this box
    def select (self):
        command  = Box.canvas + "mouse " + str(self.x-2) + " " + str(self.y-2) + " 1 0 ; "
        command += Box.canvas + "motion " + str(self.x+1) + " " + str(self.y+1) + " 0 ; "
        command += Box.canvas + "mouseup " + str(self.x+1) + " " + str(self.y+1) + " 1 0 ; "
        Box.snd.send_pd(command)
        
        for b in memory_box:
            b.selected = False
        self.selected = True
    
    #method that unselects this box
    def unselect(self):
        command  = Box.canvas + "mouse " + str(self.x-2) + " " + str(self.y-2) + " 1 0 ; "
        command += Box.canvas + "mouseup " + str(self.x-2) + " " + str(self.y-2) + " 1 0 ; "
        Box.snd.send_pd(command)
        
        for b in memory_box:
            b.selected = False
    
    #deprecated!
    #method that selects this box with key shift pressed
    def shift_select (self):
        #Box.snd.send_pd( Box.canvas + "key 1 Shift_R 0 ; " )
        #self.select()
        #Box.snd.send_pd( Box.canvas + "key 0 Shift_R 0 ; " )
        self.selected = True
        
    #deprecated!
    #method that unselects this box with key shift pressed
    def shift_unselect(self):
        #Box.snd.send_pd( Box.canvas + "key 1 Shift_R 0 ; " )
        #self.click()
        #Box.nd_pd( Box.canvas + "key 0 Shift_R 0 ; " )
        self.selected = False
        
    
    #gets the number of inlets of the object
    def verify_inlets (self):
        #import dinamico pra evitar problema de referencia ciclica
        from connection import Connection, connect
        from object import Object
        
        #building an inlet test
        inlet = Object(self.x, self.y-30, "inlet")
        finished = False
        
        #tries to connect every single inlet to the inlet above
        n_inlets = -1
        while not(finished):
            n_inlets = n_inlets+1
            #if fails on connect, finishes the interaction
            finished = not (connect(inlet, 0, self, n_inlets))
        inlet.delete()
        
        self.inlets = n_inlets
        
        return n_inlets
    
    
    #gets the number of outlets of the object
    def verify_outlets (self):
        #import dinamico pra evitar problema de referencia ciclica
        from connection import Connection, connect
        from object import Object
        
        #building an outlet test
        outlet = Object(self.x, self.y-30, "outlet")
        finished = False
        
        #tries to connect every single outlet to the outlet above
        n_outlets = -1
        while not(finished):
            n_outlets = n_outlets+1
            #if fails on connect, finishes the interaction
            finished = not (connect(self, 0, outlet, n_outlets))
        outlet.delete()
        
        self.outlets = n_outlets
        
        return n_outlets
    

        
    #aux static function to debug this class
    @staticmethod
    def debug():
        box = Box(20, 20, 0)
        print box.move(10, 10)
        print box.select()
        print box.unselect()
        print box.shift_select()
        print box.shift_unselect()
    


