import meep as mp
import numpy as np
from datetime import date
import MeepFunctions as MF
from matplotlib import pyplot as plt
import sys, getopt,os



# -r for runtime in fs
# -f for filename






#input function arguments

nOffset,filename = MF.main(sys.argv[1:])   
#print(Simtime,filename)


coreN=1
cladN=1
TL = 125
Depth=40
GAP=100


sim,src,tran = MF.buildModelSQR(coreN,cladN,TL,Depth,GAP)


t = (1e-6/3e8)
tFactor = 1e-15/t # converts femptoseconds into unitless MEEP 

Simtime = 1e5

print("Actual Simtime:", Simtime*t)

workingDir = MF.mkALLDIRS(sim,filename)



#print('figure')
plt.figure(dpi=200)
sim.plot2D(eps_parameters={'alpha':0.8, 'interpolation':'none'})
plt.savefig(workingDir+"ModelatStart.pdf")
#print('savefig')


DecayFactor = 1e-8
pt = mp.Vector3(x=0,y=0,z=0)

MF.tic()

sim.run(mp.at_beginning(mp.output_epsilon),
        mp.at_every(10500, mp.output_dpwr),
        until=(Simtime*tFactor))

#sim.run(mp.at_beginning(mp.output_epsilon),
#      mp.at_every(20000, mp.output_dpwr),
#      until_after_sources=mp.stop_when_fields_decayed(750,mp.Ez,pt,DecayFactor))


T = MF.toc()



plt.figure(dpi=200)
sim.plot2D(fields=mp.Ez,plot_sources_flag=True,plot_monitors_flag=True)
plt.savefig(workingDir+"FieldsAtEnd.pdf")

fcen = 1/1.55
df = 16
nfreq=100
resolution=10

meta = {
        "DecayFactor": DecayFactor,
        "Walltime": T,
        "Gap": GAP,
        "fsrc": fcen,
        "df": df,
        "nfreq":nfreq,
        "resolution":resolution,
        "Depth":Depth
        }

today = str(date.today())
MF.dumpData2File(meta,today,workingDir,sim,src,tran,nfreq)


fig,axes = plt.subplots(1,1,figsize=(16,9))

wl = 1/np.array(mp.get_flux_freqs(tran))

Tran = np.array(mp.get_fluxes(tran))

Src = np.array(mp.get_fluxes(src))

axes.plot(wl,Tran,label='Overall Transmission')
axes.plot(wl,Src,label='Overall Transmission')
plt.savefig(workingDir+"Spectrum.pdf")



#fig_format(axes,'','Wavelength / um','Relative Power','')





