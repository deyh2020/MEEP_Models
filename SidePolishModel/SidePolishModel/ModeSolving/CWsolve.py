from re import S
import ModeSolving.Model as M
import time as time
import numpy as np
import matplotlib.pyplot as plt
import h5py
from os import listdir


class CWsolve:

    def __init__(self):

        self.M = M.Model()
        self.M.res = 10
        self.M.FibreType = "Polished"
        self.M.SimSize = 20
        
        self.temps = np.array([23,30,40,50,60,70,80])
        self.neffPDMS = np.array([])
        self.neff     = np.array([])
        self.neffPDMS = np.array([])
           
    def run(self):

        self.M.filename = 'Air'
        self.M.nCoating = 1.00

        self.M.BuildAndSolve() #Runs CW sim and saves eps and ey fields. 
        
        self.plotFieldProfile()
        
        self.M.sim.reset_meep()
        
        
        self.M.filename = 'PDMS'
        self.M.nCoating = 1.41
        
        self.M.BuildAndSolve() #Runs CW sim and saves eps and ey fields. 
        
        self.plotFieldProfile()

        self.runNEFFexp()

        #plt.show()
    
    
    def importh5(self):
        directory = self.M.workingDir
        epsFile = "runner-eps-000000.00.h5"
        eyFile = "runner-ey-000000.00.h5"
        eps = np.flip( np.transpose( np.array( h5py.File(directory + epsFile,'r')['eps'] ) ),0 )
        ey = np.flip( np.transpose( np.array( h5py.File(directory + eyFile,'r')['ey.r'] ) ),0 )
        return eps,ey
    
    def plotFieldProfile(self):

        eps,ey = self.importh5()

        fig,axes = plt.subplots(dpi=150)

        dx = self.M.SimSize/2

        ext = (-dx,dx,-dx,dx)


        axes.imshow(ey,
                extent=ext,
                interpolation='antialiased',
                cmap='viridis',
                vmax= np.max(ey),
                vmin= 0
                )

        axes.autoscale(False)
        axes.set_xlim(-self.M.R1*1.8,self.M.R1*1.8)
        axes.set_ylim(-self.M.R1*1.8,self.M.R1*1.8)
        

        from matplotlib.patches import Circle, Rectangle
        

        circ = Circle((0,0),self.M.R1,fill=False)
        axes.add_patch(circ)

        Rect = Rectangle((-dx,self.M.R1 + self.M.Pad),2*dx,0,fill=False)
        axes.add_patch(Rect)
       
        eps = (eps - 1.00)**15  #scale the eps values to show small contrasts better
        
        """
        axes.imshow(eps,
                alpha=0.25,
                interpolation="none",
                extent=ext,
                cmap='binary',
                vmax=np.max(eps),
                vmin=0.00
                )
        """

        axes.set_xlabel("X / um",fontsize=16)
        axes.set_ylabel("Y / um",fontsize=16)
        axes.ticklabel_format(style='sci',scilimits=(-1,5),axis='both',useOffset=False)

        plt.savefig(self.M.workingDir+"FieldProfile"+ self.M.filename +".pdf")


    def runNEFFexp(self):
        
        for t in self.temps:  

            print("")
            print("Working at "+ str(t))
            print("")

            self.M.Datafile = "temp_" + str(t)

            self.M.nCoating = 1
            self.M.coreN = np.polyval(self.M.SilicaFIT,t)
            self.M.cladN = self.M.coreN - 0.005

            self.M.BuildAndSolveNEFF()

            self.neff =  np.append(self.neff,self.M.neff)


        for t in self.temps:  

            print("")
            print("Working at "+ str(t))
            print("")

            self.M.Datafile = "PDMSCoated_temp_" + str(t)

            self.M.nCoating = np.polyval(self.M.PDMSfit,t)
            self.M.coreN = np.polyval(self.M.SilicaFIT,t)
            self.M.cladN = self.M.coreN - 0.005


            self.M.BuildAndSolveNEFF()

            self.neffPDMS = np.append(self.neffPDMS,self.M.neff)


        fig,ax = plt.subplots(dpi=150)

        ax.plot(self.temps,self.neff,label="Uncoated")
        ax.plot(self.temps,self.neffPDMS,label="PDMS Coated")


        ax.set_ylabel("$n_{eff}$")
        ax.set_xlabel("Temp / C")
        plt.legend()
        plt.savefig(self.M.workingDir+"NEFF" +".pdf")