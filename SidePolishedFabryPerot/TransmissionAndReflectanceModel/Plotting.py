import Model as M
import numpy as np
import meep as mp
import matplotlib.pyplot as plt

def fig_format(ax1,Title,Xlabel,Ylabel):
    ax1.set_title(Title,fontsize=18)
    ax1.set_xlabel(Xlabel,fontsize=16)
    ax1.set_ylabel(Ylabel,fontsize=16)
    #ax1.grid(b=True, which='major', color='grey', linestyle='-',alpha=0.4)
    #ax1.grid(b=True, which='minor', color='grey', linestyle='--',alpha=0.4)
    ax1.minorticks_on()  
    #ax1.legend(title=legtitle)
    ax1.ticklabel_format(style='sci',scilimits=(-1,5),axis='both',useOffset=False)


Model = M.Model() 

Model.filename = 'Figures'

Model.GAP = 0
Model.Width = 300

Model.EllipseOffset = 20
Model.Depth = 50
Model.BubblesNum = 1

Model.res = 5
Model.nCoating = 1.00
Model.CladLeft = 2


Model.buildPolished()
Model.ADDellipseBubbles()
Model.BuildModel()

plt.show()
