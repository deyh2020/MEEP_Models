import Model as M
import numpy as np
import meep as mp


Model = M.Model() 

#mp.verbosity(2)

#Set the PDMSn = 1 for effectively a uncoated side-polished fibre.


Model.nCoating = 1.41

Model.CladLeft = 5
Model.GAP = 800
Model.Width = 1
Model.fcen   = 1/1.55
Model.df     = 1.2e-2
Model.nfreq  = 1000
Model.DecayF = 1e-8
Model.dpml = 10
Model.filename = 'FullRunTopsy'
Model.Notes    = ''

Model.monitorPts = 2
Model.res = 3

Model.buildPolished()

#do normalisation run only needs to be done once
#build model without defects



Model.BuildModel(NormRun=True,Plot=True) 

Model.NormRun()

"""

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

"""