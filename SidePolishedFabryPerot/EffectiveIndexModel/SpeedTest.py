import Model as M
import time as time
import numpy as np
import matplotlib.pyplot as plt

Model = M.Model()

#Model.nCoating = 1.000
Model.df     = 2e-2
Model.filename = 'SpeedTesting'
Model.Notes    = ''
Model.Pad = 0    #Cladding left over from polishing
Model.wl = 1.55
Model.nCoating = 1.000

Model.res = 5
Model.SimSize = 35

Model.Objlist = []
#Model.buildFibre()
Model.buildPolishedFibre()
Model.BuildModel(Plot=False) 

Model.tic()
Model.RunMPB()
Model.toc()

print("EffectiveIndex = ", Model.neff)


Model.SimT = 10
Model.RunAndPlotF()

