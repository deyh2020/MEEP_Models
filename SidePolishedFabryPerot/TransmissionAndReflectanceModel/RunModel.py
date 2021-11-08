import Model as M


Model = M.Model() 

Model.PDMSn = 1.000
Model.CladLeft = 1
Model.GAP = 100
Model.Width = 100
Model.fcen   = 1/1.55
Model.df     = 1.3e-2
Model.nfreq  = 1000
Model.res = 10
Model.DecayF = 1e-20
Model.filename = 'LargerCavityNoPDMSDblRes&Time'
Model.Notes    = ''

Model.buildPolished()




#do normalisation run
#build model without defects

Model.BuildModel(NormRun=False,Plot=False) 
Model.NormRun()



#resetMEEP
Model.sim.reset_meep()


#Build model with everything.
Model.sqrBubbles()
Model.BuildModel(NormRun=False,Plot=False) 

# for normal run, load negated fields to subtract incident from refl. fields
Model.sim.load_minus_flux_data(Model.refl, Model.norm_refl)

#Run until fields decayed by 1e3
Model.AutoRun()


