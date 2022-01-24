import Model as M



Model = M.Model() 

Model.df = 2e-2
Model.res = 10/1.55  # at least 10 px per wavelength
Model.Courant = 1


Model.GAP = 1000
Model.Mthick = 300
Model.BackgroundN = 1.41
Model.N1 = 1.00
Model.N2 = Model.N1

Model.filename = '1D_Test'
Model.Datafile = 'Wooooo'


Model.RunTRspectrum()

