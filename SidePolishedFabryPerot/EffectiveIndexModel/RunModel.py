import Model as M
import time as time

Model = M.Model()

Model.SimSize = 100
Model.PMLThick = 2

#Model.buildFibre()
Model.buildPolishedFibre()

Model.res = 1
Model.filename = 'Debugging'
Model.Notes    = 'Trying to get Bloch BC working'
Model.SrcSize  = 20


Model.BuildModel() 

#Model.GetEigenModes() #also sets sources up at the fundamental mode




Model.SimT = 100  #setSimtime in fs

#while 1:
#Model.RunAndPlotF()
#time.sleep(1)
