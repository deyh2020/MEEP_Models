import Model as M
import numpy as np
import meep as mp
import matplotlib.pyplot as plt



Model = M.Model() 

#mp.verbosity(2)

#Set the PDMSn = 1 for effectively a uncoated side-polished fibre.


Model.buildPolished()

temps = [23]

Model.filename = 'SingleBubble'

Model.GAP = 0
Model.Width = 300

for T in temps:  

    Model.Datafile = "temp_" + str(T)

    Model.nCoating = np.polyval(Model.PDMSfit,T)
    Model.coreN = np.polyval(Model.SilicaFIT,T)
    Model.cladN = Model.coreN - 0.005

    Model.BuildModel(NormRun=True,Plot=False) 

    Model.tic()
    Model.NormRun()
    Model.toc()

    #resetMEEP
    Model.sim.reset_meep()

    #Model.filename = 'SingleBubble_Temp_' + str(T)

    Model.Objlist = []

    #Build model with everything.
    Model.sqrBubbles(Num=1)
    Model.BuildModel(NormRun=False,Plot=True) 
    # for normal run, load negated fields to subtract incident from refl. fields
    Model.sim.load_minus_flux_data(Model.refl, Model.norm_refl)
    
    #Run until fields decayed by 1e3
    #Model.tic()
    Model.AutoRun()
    #Model.toc()
    Model.SaveMeta()

plt.show()


