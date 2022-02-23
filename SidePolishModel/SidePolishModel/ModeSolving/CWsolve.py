import Model as M
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

    def importh5(self,dir):
        epsFile = "CWsolve-" + self.M.filename + "-eps-000000.00.h5"
        eps = np.flip( np.transpose( np.array( h5py.File(dir + epsFile,'r')['eps'] ) ),0 )

        print(eps)

    
    def plot(self):
        WD = self.M.workingDir + self.M.filename

        eps,ey = self.importh5(WD)




