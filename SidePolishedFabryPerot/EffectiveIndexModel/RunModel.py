import Model as M
import time as time

Model = M.Model()


Model.res = 5
Model.filename = 'Debugging'
Model.Notes    = 'Trying to get Bloch BC working'
#Model.SrcSize  = 20

Model.Pad = 0       #Cladding left over from polishing


Model.buildFibre()
#Model.buildPolishedFibre(WPDMS=False)

Model.BuildModel(Plot=False) 

#Model.GetEigenModes() #also sets sources up at the fundamental mode

Model.RunKpoints()


#Model.SimT = 100  #setSimtime in fs

#while 1:
#Model.RunAndPlotF()
#time.sleep(1)
