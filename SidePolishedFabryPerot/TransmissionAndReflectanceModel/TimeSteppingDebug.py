import Model as M
import numpy as np
import matplotlib.pyplot as plt
import meep as mp

Model = M.Model() 

print(Model.sim)


#Set the PDMSn = 1 for effectively a uncoated side-polished fibre.

Model.GAP = 0
Model.Width = 300
Model.Depth = Model.R1 + Model.R2 + 4
Model.BubblesNum = 1

Model.filename = 'ElongatedCircTest'


Model.df = 0.042
#Model.res = 4





Model.Objlist = []	
Model.buildNormalfibre()
Model.ADDcircElongated()

Model.BuildModel(NormRun=False,Plot=False) 


Model.SimT = 38000

Model.sim.run(
    mp.at_beginning(mp.output_epsilon),
    mp.at_every(500, mp.output_dpwr),
    until=Model.SimT

)
