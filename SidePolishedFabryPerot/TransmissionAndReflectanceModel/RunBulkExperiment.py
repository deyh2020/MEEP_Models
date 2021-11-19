import Model as M
import numpy as np


Model = M.Model() 


#Set the PDMSn = 1 for effectively a uncoated side-polished fibre.

#Model.PDMSn = 1.00

Model.CladLeft = 5
Model.GAP = 1000
Model.Width = 100
Model.fcen   = 1/1.55
Model.df     = 1.2e-2
Model.nfreq  = 1000
Model.res = 5
Model.DecayF = 1e-4
Model.filename = 'CoatedvsUncoated'
Model.Notes    = ''

Model.buildPolished()

#do normalisation run only needs to be done once
#build model without defects

Model.BuildModel(NormRun=False,Plot=False) 
Model.NormRun()



Model.filename = 'PDMSCoated'
Model.Datafile = "Data"

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



Model.sim.reset_meep()

Model.filename = 'UNCoated'
Model.Datafile = "Data"
Model.PDMSn = 1.00


Model.buildPolished()

#do normalisation run only needs to be done once
#build model without defects

Model.BuildModel(NormRun=False,Plot=False) 
Model.NormRun()

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

