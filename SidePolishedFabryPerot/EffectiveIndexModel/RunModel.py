import Model as M
import time as time

Model = M.Model() 

Model.SimSize = 60
Model.PMLThick = 2

Model.buildFibre()

Model.res = 3
Model.filename = 'Debugging'
Model.Notes    = 'Trying to get Bloch BC working'


Model.BuildModel() 

Model.SimT = 100  #setSimtime in fs

#Model.GetEigenModes()

Model.RunKpoints()

#while 1:
#Model.RunAndPlotF()
#time.sleep(1)
