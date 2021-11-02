import Model as M
import time as time
import numpy as np

Model = M.Model()

Model.df     = Model.fcen*1000
Model.res = 10
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


wi = Model.harm.modes[0].decay * (2*np.pi/a) 

vg = Model.vg  * c     # grab group v and convert to m/s

print('wi',wi)
print('vg',vg)

lam = 1.55e-6

k0 = 2*np.pi/lam
k  = 1/Model.kpoint.z * 2*np.pi/a

print('k0',k0)
print('k',k)

bi = wi/vg

b = complex(k,bi)

print("")

#print("Propagation Constant =",b)

neff = b/k0

print("n_eff =",neff)


#while 1:
#Model.RunAndPlotF()
#time.sleep(1)
