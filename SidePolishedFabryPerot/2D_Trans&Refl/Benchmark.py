import Model as M
import numpy as np
import meep as mp
import matplotlib.pyplot as plt



Model = M.Model() 

#mp.verbosity(2)

#Set the PDMSn = 1 for effectively a uncoated side-polished fibre.


Model.filename = 'Benchmarks'

Model.df = 0.5e-2
Model.res = 10/1.55  # at least 10 px per wavelength
Model.Courant = 1/np.sqrt(2)
Model.fcen = 1/1.60

#Model.TestSpectrum()

#plt.show()

 
Model.Datafile = "Bench"

Model.nCoating = 1.00

Model.RunTRspectrum()



#plt.show()
