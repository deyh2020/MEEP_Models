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
        plt.show()
    
    
    
    
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
        axes.set_xlim(-self.M.R1*1.75,self.M.R1*1.75)
        axes.set_ylim(-self.M.R1*1.75,self.M.R1*1.75)
        

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



    