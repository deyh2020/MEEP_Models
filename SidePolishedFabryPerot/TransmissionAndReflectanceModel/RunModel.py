import Model as M


Model = M.Model() 


Model.CladLeft = 1
Model.GAP = 100

Model.fcen   = 1/1.55
Model.df     = 50
Model.nfreq  = 10
Model.res = 5
Model.DecayF = 1e-4
Model.filename = 'No Bubbles'
Model.Notes    = 'Only Polished'

Model.buildPolished()




#do normalisation run
#build model without defects

Model.BuildModel(NormRun=False,Plot=False) 
Model.NormRun()



#resetMEEP
Model.sim.reset_meep()


#Build model with everything.
Model.addtriBubbles()
Model.BuildModel(NormRun=False,Plot=False) 

# for normal run, load negated fields to subtract incident from refl. fields
Model.sim.load_minus_flux_data(Model.refl, Model.norm_refl)

#Run until fields decayed by 1e3
Model.AutoRun()


