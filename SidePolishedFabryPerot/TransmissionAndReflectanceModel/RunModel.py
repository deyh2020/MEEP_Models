import Model as M


Model = M.Model() 



Model.buildFibre()

Model.res = 4
Model.filename = 'TestRunPC'
Model.Notes    = 'Post object orientated recode.'

Model.addtriBubbles()
#Model.addSQRBubbles()

Model.BuildModel() 

Model.SimT = 1e4  #setSimtime in fs

Model.RunSetT()


