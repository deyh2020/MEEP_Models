import meep as mp
import numpy as np
import matplotlib.pyplot as plt
import sys, getopt,os
from datetime import date
import pickle,json, os




def buildModel(coreN,cladN,TL,Depth,GAP):
    cell_size = mp.Vector3(400,70,0)

    pml_layers = [mp.PML(thickness=4)]

    

    PDMS = mp.Block(
                   center=mp.Vector3(0,0,0),
                   size=mp.Vector3(mp.inf,mp.inf,mp.inf),
                   material=mp.Medium(index=PDMSn)
                    )

    Clad = mp.Block(
                   center=mp.Vector3(x=0,y=(-62.5/2 +5),z=0),
                   size=mp.Vector3(x=mp.inf,y=62.5,z=mp.inf),
                   material=mp.Medium(index=1.4402)
                    )

    Core = mp.Block(
                   center=mp.Vector3(0,0,0),
                   size=mp.Vector3(mp.inf,8.2,mp.inf),
                   material=mp.Medium(index=1.4452)
                    )


    r1 = 4.1
    r2 = 62.5
    RW=1

    verts = [
            
            mp.Vector3(x=-(RW/2+TL/2) ,y=r2 ,z=0)   ,
            mp.Vector3(x=(RW/2+TL/2)  ,y=r2 ,z=0)  ,
            mp.Vector3(x=(RW/2)       ,y=r2-Depth ,z=0)   ,
             mp.Vector3(x=-(RW/2)      ,y=r2-Depth ,z=0)
        
            ]


    LH = mp.Prism(center=mp.Vector3(x=-GAP/2,y=0,z=0),
                     vertices = verts,
                     material=mp.Medium(index=PDMSn),
                     height=1
                     )

    RH = mp.Prism(center=mp.Vector3(x=GAP/2,y=0,z=0),
                     vertices = verts,
                     material=mp.Medium(index=PDMSn),
                     height=1
                     )




    geometry = [PDMS,Clad,Core,LH,RH]

    fcen = 1/1.55
    df = 16


    kx = 0.4    # initial guess for wavevector in x-direction of eigenmode
    kpoint = mp.Vector3(kx)
    bnum = 1    # band number of eigenmode

    src = [mp.EigenModeSource(src=mp.GaussianSource(fcen,fwidth=df),
                                  center=mp.Vector3(x=-195,y=0),
                                  size=mp.Vector3(y=40),
                                  direction=mp.X,
                                  eig_kpoint=kpoint,
                                  eig_band=bnum,
                                  #eig_parity=mp.EVEN_Y+mp.ODD_Z,
                                  eig_match_freq=True)]

    symmetries = [mp.Mirror(mp.Y,phase=+1)]

    sim = mp.Simulation(cell_size=cell_size,
                        geometry=geometry,
                        sources=src,
                        resolution=2,
                        force_complex_fields=False,
                        #symmetries=symmetries,
                        boundary_layers=pml_layers,
                        #k_point=mp.Vector3(mp.X)
                       )


    # src flux
    src_fr = mp.FluxRegion(center=mp.Vector3(-150,0,0), size=mp.Vector3(0,40,0))                            
    src = sim.add_flux(fcen, 8e-3, 100, src_fr)



    # transmitted flux
    tran_fr = mp.FluxRegion(center=mp.Vector3(150,0,0), size=mp.Vector3(0,40,0))
    tran = sim.add_flux(fcen, 8e-3, 100, tran_fr)

    return sim,src,tran

def buildModelSQR(coreN,cladN,TL,Depth,GAP):
    cell_size = mp.Vector3(400,70,0)

    pml_layers = [mp.PML(thickness=4)]

    PDMSn = 1.41
    
    r1 = 4.1
    r2 = 62.5
    
    Width = 62.5    # width of bubbles
    CladLeft = 5   # amount of cladding left from initial polish (thickness of cladding before getting to the core.
    

    PDMS = mp.Block(
                   center=mp.Vector3(0,0,0),
                   size=mp.Vector3(mp.inf,mp.inf,mp.inf),
                   material=mp.Medium(index=PDMSn)
                    )
    
    
    

    Clad = mp.Block(
                   center=mp.Vector3(x=0,y=(-r2/2 + CladLeft),z=0),
                   size=mp.Vector3(x=mp.inf,y=r2,z=mp.inf),
                   material=mp.Medium(index=1.4402)
                    )

    
    
    Core = mp.Block(
                   center=mp.Vector3(0,0,0),
                   size=mp.Vector3(mp.inf,2*r1,mp.inf),
                   material=mp.Medium(index=1.4452)
                    )
    
    
    LH = mp.Block(
                   center=mp.Vector3(x=-GAP/2,y=-(Depth/2 - 2*r1 - CladLeft),z=0),
                   size=mp.Vector3(Width,Depth,mp.inf),
                   material=mp.Medium(index=PDMSn)
                    )
    RH = mp.Block(
                   center=mp.Vector3(x=GAP/2,y=-(Depth/2 - 2*r1 - CladLeft),z=0),
                   size=mp.Vector3(Width,Depth,mp.inf),
                   material=mp.Medium(index=PDMSn)
                    )



    geometry = [PDMS,Clad,Core,LH,RH]

    fcen = 1/1.55
    df = 16


    kx = 0.4    # initial guess for wavevector in x-direction of eigenmode
    kpoint = mp.Vector3(kx)
    bnum = 1    # band number of eigenmode

    src = [mp.EigenModeSource(src=mp.GaussianSource(fcen,fwidth=df),
                                  center=mp.Vector3(x=-195,y=0),
                                  size=mp.Vector3(y=40),
                                  direction=mp.X,
                                  eig_kpoint=kpoint,
                                  eig_band=bnum,
                                  #eig_parity=mp.EVEN_Y+mp.ODD_Z,
                                  eig_match_freq=True)]

    symmetries = [mp.Mirror(mp.Y,phase=+1)]

    sim = mp.Simulation(cell_size=cell_size,
                        geometry=geometry,
                        sources=src,
                        resolution=10,
                        force_complex_fields=False,
                        #symmetries=symmetries,
                        boundary_layers=pml_layers,
                        #k_point=mp.Vector3(mp.X)
                       )


    # src flux
    src_fr = mp.FluxRegion(center=mp.Vector3(-150,0,0), size=mp.Vector3(0,40,0))                            
    src = sim.add_flux(fcen, 8e-3, 100, src_fr)



    # transmitted flux
    tran_fr = mp.FluxRegion(center=mp.Vector3(150,0,0), size=mp.Vector3(0,40,0))
    tran = sim.add_flux(fcen, 8e-3, 100, tran_fr)

    return sim,src,tran


def dumpData2File(meta,today,workingDir,sim,src,tran,nfreq):
    
    # initialise main data dictionary
    Data = {}
    Data['Src'] = {}       # sensor just after source.
    Data['Out'] = {}       # sensor at the end of the WG (for transmission)
    
    
    Data['Src']['lambda'] = 1/np.array(mp.get_flux_freqs(src))
    Data['Src']['flux'] = np.array(mp.get_fluxes(src))
    
    Data['Out']['lambda'] = 1/np.array(mp.get_flux_freqs(tran))
    Data['Out']['flux'] = np.array(mp.get_fluxes(tran))
    

    metadata = {
        "date": str(today),
        "Data": workingDir+"Data.pk1"
    }

    metadata = {**metadata,**meta}
    

    with open(metadata['Data'], 'wb') as file:
        pickle.dump(Data,file)


    with open(workingDir + 'metadata.json', 'w') as file:
        json.dump(metadata, file)
        
        
        
def main(argv):
   offset = 0
   filename = 'test'
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('test.py -i <nOffset> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('test.py -i <nOffset> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         offset = float(arg)
      elif opt in ("-o", "--ofile"):
         filename = str(arg)
   return offset,filename


def mkALLDIRS(sim,filename):
    
    today = str(date.today())

    workingDir = 'data/'+today+'/'+filename+'/'

    print('WD:',workingDir)

    try:
        os.makedirs(workingDir)
    except:
        print('AlreadyDir')

    sim.use_output_directory(workingDir)
    return workingDir

import time

def TicTocGenerator():
    # Generator that returns time differences
    ti = 0           # initial time
    tf = time.time() # final time
    while True:
        ti = tf
        tf = time.time()
        yield tf-ti # returns the time difference

TicToc = TicTocGenerator() # create an instance of the TicTocGen generator

# This will be the main function through which we define both tic() and toc()
def toc(tempBool=True):
    # Prints the time difference yielded by generator instance TicToc
    tempTimeInterval = next(TicToc)
    if tempBool:
        return tempTimeInterval

def tic():
    # Records a time in TicToc, marks the beginning of a time interval
    toc(False)


