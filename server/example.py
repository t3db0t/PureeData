

##########################################################
##########################################################
# description: example that works with connection/disconnections of boxes
#
# autor: jeraman
# date: 26/04/2010
##########################################################
##########################################################

#imports Pyata library
from Pd import *
import math
import datetime



#planet class for rotate boxes
class Clock():
    def __init__(self, radius, c_x, c_y, center, inlet=0):
        self.radius = radius
        self.center = center
        self.inlet = inlet
        self.list = []
        self.draw()
        self.pointer = 0
        
    def increment(self):   
        disconnect(self.list[self.pointer], 0, self.center, self.inlet)
        self.pointer = (self.pointer+1)%12 
        connect(self.list[self.pointer], 0, self.center, self.inlet)
    
    def draw(self):
        q_boxes = 12
        total = 360
        slice_angle = total/q_boxes
        angle = -90 - slice_angle
        
        for i in range(0,q_boxes+1):
            angle += slice_angle
            rad_angle = math.radians(angle)
            x = self.radius * math.cos(rad_angle)
            y = self.radius * math.sin(rad_angle)
            x+=self.center.x
            y+=self.center.y
            x = int(x)
            y = int(y)
            n = Number(x, y)
            n.set(i)
            self.list.append(n)


#mains method
if __name__ == '__main__':
    #creates an instance of Pd
    pd = Pd()
    
    #initializes Pyata
    pd.init()
    
    #creates a center
    centro = Object(300, 300, "outlet")

    c1=Clock(100, 300, 300, centro)
    c2=Clock(300, 300, 300, centro)
    
    #varibles to stores the second
    s = 0
    
    #runs during 20 seconds
    for i in range (40):
        s = (s+1)%12
        c1.increment()
        if s==0:
            c2.increment()
        sleep(0.5)

    #finishes Pyata
    pd.quit()
    
   