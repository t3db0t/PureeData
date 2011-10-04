from Pd import *

#mains method
if __name__ == '__main__':
    
    #creates an instance of Pd
    pd = Pd()
    
    #initializes Pyata
    pd.init()
    
    #creates a bang
    bang = Message(300, 100, "bang")
    #creates a random object
    rand = Object(300, 200, "random 100")
    #creates a number
    n = Number(300, 300)
    
    #connects the bang to the random
    connect(bang, 0, rand, 0)
    #connects the outlet from radom to a number
    connect(rand, 0, n, 0)
    
    #repeat 20 times
    for i in range(1, 20):
        #bangs 
        bang.click()
        #gets the updated value form number
        print n.get_value()
        #sleeps a second
        sleep(1)
    
    #finishes Pyata
    pd.quit()