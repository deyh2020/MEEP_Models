import Model as M
import time as time
import numpy as np

Model = M.Model()

Model.df     = Model.fcen*1000
Model.res = 4
Model.filename = 'Debugging'
Model.Notes    = 'Trying to get Bloch BC working'


Model.Pad = 0       #Cladding left over from polishing


Model.buildFibre()
#Model.buildPolishedFibre(WPDMS=True)

Model.BuildModel(Plot=False) 

#Model.GetEigenModes() #also sets sources up at the fundamental mode

#Model.SimT = 100  #setSimtime in fs
#Model.RunAndPlotF()

#Model.RunKpoints()
Model.RunHarmv()

a = 1e-6
c = 2.99e8

wi = Model.harm.modes[0].decay 
vg = Model.vg 

b = (wi/vg) * 2*np.pi/a

print("Calculated B: ",b)


neff = b*(1.55e-6/(2 * np.pi))
print("Calculated Neff: ",neff)


#while 1:
#Model.RunAndPlotF()
#time.sleep(1)
