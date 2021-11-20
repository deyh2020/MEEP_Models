import Model as M
import numpy as np
import matplotlib.pyplot as plt
import meep as mp

Model = M.Model() 

print(Model.sim)


#Set the PDMSn = 1 for effectively a uncoated side-polished fibre.

Model.CladLeft = 5
Model.GAP = 1000
Model.Width = 100
Model.fcen   = 1/1.55
Model.df     = 1.2e-2
Model.nfreq  = 1000
Model.res = 3
Model.DecayF = 1e-10
Model.filename = 'CoatedvsUncoated'
Model.Notes    = ''



#Model.PDMSn = 1.00
Model.buildPolished()



#do normalisation run only needs to be done once
#build model without defects

#Model.sqrBubbles(Num=2)

#Model.PDMSn = 1.000
Model.BuildModel(Plot=False) 


Model.SimT = 1000

while True:
    Model.TimestepFields()
