import ModeSolving.Model as M
import time as time
import numpy as np
import matplotlib.pyplot as plt
import h5py
from os import listdir


class CWsolve:

    def __init__(self):

        self.M = M.Model()
        self.M.filename = 'Air'
        self.M.res = 4
        self.M.FibreType = "Polished"
        self.M.nCoating = 1.00
           
    def run(self):
        self.M.BuildAndSolve() #Runs CW sim and saves eps and ey fields. 

    def importh5(self):
        directory = self.M.workingDir
        epsFile = "runner" + "-eps-000000.00.h5"
        eyFile = "runner" + "-ey-000000.00.h5"
        eps = np.flip( np.transpose( np.array( h5py.File(directory + epsFile,'r')['eps'] ) ),0 )
        ey = np.flip( np.transpose( np.array( h5py.File(directory + eyFile,'r')['ey.r'] ) ),0 )
        return eps,ey
    
    def plot(self):

        eps,ey = self.importh5()

        fig,axes = plt.subplots(dpi=200)

        ext = (-10,10,-10,10)

        axes.imshow(ey,
                extent=ext,
                cmap='RdBu',
               vmax= np.max(ey),
                vmin= -np.max(ey)
                )
        

        eps = (eps - 1.00)**15  #scale the eps values to show small contrasts better
        
        axes.imshow(eps,
                alpha=0.5,
                interpolation="none",
                extent=ext,
                cmap='binary',
                vmax=np.max(eps),
                vmin=1.00
                )

        plt.show()
