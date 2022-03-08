import TwoDimensionTR.Model as M
import matplotlib.pyplot as plt
import csv
import numpy as np



class TwoDsolve: 

    def __init__(self):

        self.M = M.Model()

        self.M.filename = '2mm'
        self.M.Datafile = 'Test'

        self.Air  = 1.000
        self.Core = 1.445
        self.Clad = 1.440
        self.PDMS = 1.410 

        
        self.M.Pad           = 50
        self.M.BackgroundN   = self.Core  
        self.M.N1            = self.Air

        self.M.GAP           = 10
        self.M.Width         = 322
        self.M.Depth         = 55.7
        self.M.angle         = 121.4

        #self.M.N2          = self.M.N1     

        self.M.res           = 10/1.55  # at least 10 px per wavelength
        self.M.df            = 7e-2#1.85e-2
        self.M.Courant       = 1/np.sqrt(2)

        


    def run(self):

        #self.mode_1()
        #self.mode_2(    
        #self.plotEXP()
        #self.full2D()
        self.M.buildPolished()
        self.M.ADDtrapazoidBubbles()
        self.M.BuildModel(NormRun=False,Plot=True) 
        plt.show()


    def full2D(self):

        self.M.Datafile    = 'All'
        self.M.nCoating    = self.Air
        
        
        self.M.RunTRspectrum()



    def plotEXP(self):
        filename = "../data/Experimental/FPRS without PDMS coated/0_5.csv"
        wlLine = 14
        pwrLine = 15

       

        with open(filename, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            line = 0
            for row in spamreader:
                #print(line)
                if line == wlLine:
                    wl = np.array(row,dtype=float)

                if line == pwrLine:
                    Ts = np.array(row,dtype=float)  
                    
                               
                line += 1 
        
        
        ax2 = self.M.axes.twinx()
        
        color = 'tab:red'
        ax2.plot(wl,Ts,color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.set_ylabel('db', color=color)


    def plotSim(self):
        print("Not Complete")
