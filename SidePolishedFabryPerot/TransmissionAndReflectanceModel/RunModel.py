import Model as M


Model = M.Model() 


Model.CladLeft = 1

Model.buildFibre()

Model.res = 5
Model.filename = 'TestRunPC'
Model.Notes    = 'Messing'

Model.addtriBubbles()
#Model.addSQRBubbles()

Model.BuildModel(Plot=True) 

Model.SimT = 1e4  #setSimtime in fs

#Model.RunSetT()


