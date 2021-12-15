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
Model.Depth = 55
Model.BubblesNum = 1

Model.res = 4
Model.nCoating = 1.41
Model.CladLeft = 2


Model.buildPolished()
Model.ADDellipseBubbles()
Model.BuildModel()



fig,ax = plt.subplots(dpi=150)

Model.sim.plot2D(ax=ax,
                 plot_sources_flag=False,
                 plot_monitors_flag=False,
                 plot_boundaries_flag=False,
                 eps_parameters={'alpha':0.8, 
                                 'interpolation':'none',
                                 'cmap':'binary'},
                 )

fig_format(ax,"","X / um","Y / um")

ax.set_xlim(-220,220)

plt.savefig(Model.workingDir+"Model_" + str(Model.Datafile) +".pdf")
plt.show()


