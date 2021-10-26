import Model as M
import time as time

Model = M.Model()

Model.SimSize = 6
Model.PMLThick = 1

Model.buildTestWG()

#Model.buildFibre()

Model.res = 40
Model.filename = 'Debugging'
Model.Notes    = 'Trying to get Bloch BC working'



Model.BuildTestModel() 

Model.GetEigenModes()



Model.SimT = 1500  #setSimtime in fs

#while 1:
Model.RunAndPlotF()
#time.sleep(1)
