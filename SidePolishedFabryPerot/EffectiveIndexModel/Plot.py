import Model as M
import time as time
import numpy as np
import matplotlib.pyplot as plt

Model = M.Model()


Model.filename = 'ModelTrio'
Model.Notes    = ''

Model.res = 10
Model.SimT=1

fig,ax = plt.subplots(2,3,dpi=150)

ax[0,0].set_title("Standard Fibre")
ax[0,1].set_title("Side Polished Fibre")
ax[0,2].set_title("SP and PDMS Coated")


"""
Polished and PDMS coated
"""


PDMSneff = []
Model.nCoating = 1.41

Model.tic()


Model.Datafile = "PDMSCoated"

#Change indexes 
Model.nCoating = 1.41

Model.Objlist = []
Model.buildPolishedFibre()
Model.BuildModel(Plot=True,axes=ax[0,2]) 
#Model.RunMPB()
Model.sim.reset_meep()  

Model.toc()


"""
#Polished and Un-Coated Model
"""

Uncoatedneff = []
Model.nCoating = 1.00

Model.Datafile = "Uncoated"


Model.Objlist = []
#Model.buildFibre()
Model.buildPolishedFibre()
Model.BuildModel(Plot=True,axes=ax[0,1]) 
#Model.RunMPB()
Model.sim.reset_meep()  


"""
#Standard SMF-28 Fibre
"""

NormalFibre = []
Model.nCoating = 1.00

Model.Datafile = "NormalFibre"

Model.Objlist = []
Model.buildFibre()
Model.BuildModel(Plot=True,axes=ax[0,0]) 
#Model.RunMPB()
#Model.SaveMeta()

#####################################################################################

Model = M.Model()


Model.filename = 'ModelTrio'
Model.Notes    = ''

Model.res = 10
"""
Polished and PDMS coated
"""


PDMSneff = []
Model.nCoating = 1.41

Model.tic()


Model.Datafile = "PDMSCoated"

#Change indexes 
Model.nCoating = 1.41

Model.Objlist = []
Model.buildPolishedFibre()
Model.BuildModel(Plot=False,axes=ax[1,2])
Model.RunAndPlotF(axes=ax[1,2])
#Model.RunMPB()
Model.sim.reset_meep()  

Model.toc()


"""
#Polished and Un-Coated Model
"""

Uncoatedneff = []
Model.nCoating = 1.00

Model.Datafile = "Uncoated"


Model.Objlist = []
#Model.buildFibre()
Model.buildPolishedFibre()
Model.BuildModel(Plot=False,axes=ax[1,1]) 
Model.RunAndPlotF(axes=ax[1,1])
#Model.RunMPB()
Model.sim.reset_meep()  


"""
#Standard SMF-28 Fibre
"""

NormalFibre = []
Model.nCoating = 1.00

Model.Datafile = "NormalFibre"

Model.Objlist = []
Model.buildFibre()
Model.BuildModel(Plot=False,axes=ax[1,0]) 
Model.RunAndPlotF(axes=ax[1,0])
#Model.RunMPB()
#Model.SaveMeta()
plt.show()