import Model as M
import time as time
import numpy as np
import matplotlib.pyplot as plt

Model = M.Model()


Model.filename = 'FieldProfiles'
Model.Notes    = ''

Model.res = 4



Model.FibreType = "Polished"
Model.nCoating = 1.41
Model.BuildAndSolve()



