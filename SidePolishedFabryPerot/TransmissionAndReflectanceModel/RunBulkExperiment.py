import Model as M
import numpy as np


Model = M.Model() 


#Set the PDMSn = 1 for effectively a uncoated side-polished fibre.
#Model.PDMSn = 1.41


Model.CladLeft = 5
Model.GAP = 1000
Model.Width = 100
Model.fcen   = 1/1.55
Model.df     = 1.2e-2
Model.nfreq  = 1000
Model.res = 5
Model.DecayF = 1e-1
Model.filename = 'LargerDeviceWPDMS'
Model.Notes    = ''

Model.buildPolished()




#do normalisation run only needs to be done once
#build model without defects

Model.BuildModel(NormRun=False,Plot=False) 
Model.NormRun()




gaps = np.arange(500,5000,500)


g = 150

Model.GAP = g
Model.filename = 'GapSweep_GAP: ' + str(g)
Model.Datafile = str(g)

#resetMEEP
Model.sim.reset_meep()
#Build model with everything.
Model.sqrBubbles(Num=2)
Model.BuildModel(NormRun=False,Plot=False) 



# for normal run, load negated fields to subtract incident from refl. fields
Model.sim.load_minus_flux_data(Model.refl, Model.norm_refl)

#Run until fields decayed by 1e3
Model.AutoRun()

Model.SaveMeta()

