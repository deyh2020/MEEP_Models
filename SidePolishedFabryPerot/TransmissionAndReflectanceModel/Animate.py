import Model as M
import numpy as np
import matplotlib.pyplot as plt
import meep as mp

Model = M.Model() 

print(Model.sim)


#Set the PDMSn = 1 for effectively a uncoated side-polished fibre.

Model.Width = 300
Model.Depth = Model.R1 + Model.R2 + 4
Model.BubblesNum = 1
Model.BubblesType = 'ellipse'  # cand be sqr, tri, ellipse

Model.df = 0.042
Model.res = 10


Model.filename = 'animationDebugging'


Model.Objlist = []	
Model.buildNormalfibre()
Model.ADDcircElongated()

Model.BuildModel(NormRun=False,Plot=False) 


Model.SimT = 10000

Model.run(mp.at_every(200, mp.output_efield_z), until=Model.SimT)
