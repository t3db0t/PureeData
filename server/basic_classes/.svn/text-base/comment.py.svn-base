
##########################################################
##########################################################
# description: abstract class that represents a comment box
#
# autor: jeraman
# date: 14/04/2010
##########################################################
##########################################################


from box import *

#number class itself
class Comment (Box):
    #constructor
    def __init__(self, x, y,text, id=-1):
        self.text = text
        Box.__init__(self,x, y, id)
    
    def create(self):
        command = Box.canvas + "text " + str(self.x) + " " + str(self.y) + " " + self.text + "; "
        Box.snd.send_pd(command)
        Box.create(self)

    #edits this object
    def edit(self, text):
        self.unselect() #unselects
        self.click() #selects this
        
        command = ""
        for i in text: #sends all key pressed
            command += Box.canvas + "key 1 " + str(ord(i)) + " 0 ; " 
            command += Box.canvas + "key 0 " + str(ord(i)) + " 0 ; "        
        Box.snd.send_pd(command)
        self.unselect() #unselects this
        #ajeita o indice atual do objeto na memoria do pd
        temp = memory_box.pop(search_box(self))
        memory_box.append(temp)
        
        self.text = text    
    

    #aux static function to debug this class
    @staticmethod
    def debug():
        box = Comment(20, 20, "alo!", 0)
        print box.edit("ola")