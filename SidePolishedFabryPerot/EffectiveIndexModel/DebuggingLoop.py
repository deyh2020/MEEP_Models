import Model as M
import time as time
import numpy as np
import matplotlib.pyplot as plt

Model = M.Model()


Model.filename = 'ModelTrio'
Model.Datafile = "NormalFibre"
Model.Notes    = ''

Model.res = 5



fig,axes = plt.subplots(1,2,dpi=200)

Types = ['Polished','Polished']
ncoating = [1.00,1.41]




for i in [0,1]:

    Model.FibreType = Types[i]
    Model.nCoating = ncoating[i]
    Model.BuildAndSolve(axes=axes[i])
    axes[i].set_xlabel("")
    axes[i].set_ylabel("")

axes[0].set_title("a)")
axes[1].set_title("b)")


fig.text(0.5, 0.13, 'xPos / um', ha='center')
fig.text(0.04, 0.5, 'yPos / um', va='center', rotation='vertical')

axes[1].set_yticks([])

plt.savefig(Model.workingDir+"ModeProfiles"+ str(Model.Datafile) +".pdf")
plt.show()