import Model as M
import time as time
import numpy as np
import matplotlib.pyplot as plt

Model = M.Model()


Model.filename = 'Debugging'
Model.Notes    = 'Trying to get Bloch BC working'




Model.nCoating = 1.41

Model.buildPolishedFibre()
Model.BuildModel(Plot=False) 

Model.tic()
Model.RunMPB()
Model.toc()

Model.RunAndPlotF()

Model.SaveMeta()

print("Neff",Model.neff)





"""

PDMSneff = []

for n in Model.nPDMS:  
    Model.nCoating = n
    Model.Objlist = []
    #Model.buildFibre()
    Model.buildPolishedFibre()
    Model.BuildModel(Plot=False) 
    Model.RunMPB()
    PDMSneff.append(Model.neff)
    Model.sim.reset_meep()  


neff = []
Model.nCoating = 1.000

for n in Model.nSilica:  
    Model.coreN = n
    Model.cladN = n - 0.005
    Model.Objlist = []
    #Model.buildFibre()
    Model.buildPolishedFibre()
    Model.BuildModel(Plot=False) 
    Model.RunMPB()
    neff.append(Model.neff)
    Model.sim.reset_meep()  


neff = np.array([neff])[0,:]
neff = neff - neff[0]
PDMSneff = np.array([PDMSneff])[0,:]
PDMSneff = PDMSneff - PDMSneff[0]







fig,ax = plt.subplots(dpi=150)

ax.plot(Model.PDMStemp,PDMSneff*1e3)

ax.plot(Model.Silicatemp,neff*1e3)
#ax.set_ylim(Model.cladN,Model.coreN)
ax.set_xlim(20,80)

ax.set_ylabel("$\Delta n_{eff}$ / $1e-3$")
ax.set_xlabel("Temp / C")

plt.show()

"""