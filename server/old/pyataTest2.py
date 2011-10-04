from Pd import *

#mains method
if __name__ == '__main__':
    
    #creates an instance of Pd
    pd = Pd()
    
    #initializes Pyata
    pd.init(usePdThread=False)
    
    lsend = Object(300, 400, "send~ left")
    rsend = Object(350, 400, "send~ right")
    
    osc = Object(300, 300, "osc~ 440")
    
    connect(osc, 0, lsend, 0)
    connect(osc, 0, rsend, 0)
    
    sleep(1200)