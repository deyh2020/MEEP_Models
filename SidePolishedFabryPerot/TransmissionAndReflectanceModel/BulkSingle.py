import Model as M
import numpy as np
import meep as mp
import matplotlib.pyplot as plt



Model = M.Model() 

#mp.verbosity(2)

#Set the PDMSn = 1 for effectively a uncoated side-polished fibre.

temps = [20,40,60,80]

Model.filename = 'NowChangeTemp'

Model.GAP = 0
Model.Width = 100
Model.BubblesNum = 1

for T in temps:  

    Model.Datafile = "Coated_temp_" + str(T)

    Model.nCoating = np.polyval(Model.PDMSfit,T)
    Model.coreN = np.polyval(Model.SilicaFIT,T)
    Model.cladN = Model.coreN - 0.005
    
    Model.RunTRspectrum()

    Model.Datafile = "Uncoated_temp_" + str(T)

    Model.nCoating = 1.00
    Model.coreN = np.polyval(Model.SilicaFIT,T)
    Model.cladN = Model.coreN - 0.005
    
    Model.RunTRspectrum()




#plt.show()


