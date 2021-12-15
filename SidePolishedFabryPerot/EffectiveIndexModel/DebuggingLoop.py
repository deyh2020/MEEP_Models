import Model as M
import time as time
import numpy as np
import matplotlib.pyplot as plt

Model = M.Model()


Model.filename = 'ModelTrio'
Model.Notes    = ''

Model.res = 3
Model.SimT=19



Model.nCoating = 1.00

Model.Datafile = "NormalFibre"

Model.Objlist = []
Model.buildFibre()
Model.BuildModel_CW(Plot=False) 
Model.RunAndPlotF_FDS()

"""

Model.sim.reset_meep() 


PDMSneff = []
Model.nCoating = 1.00


Model.Datafile = "PDMSCoated"

#Change indexes 
Model.nCoating = 1.41

Model.Objlist = []
Model.buildPolishedFibre()
Model.BuildModel_CW(Plot=False) 
Model.RunAndPlotF_FDS()

"""

plt.show()