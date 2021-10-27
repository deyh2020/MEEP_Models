import meep as mp
import numpy as np
import matplotlib.pyplot as plt
import sys, getopt,os
from datetime import date
import pickle,json, os
import time



class Model:

	def __init__(self):

		#init constants
		
		##Material N
		self.PDMSn  = 1.41
		self.coreN  = 1.445
		self.cladN  = 1.440

		##Fibre Dimentions
		self.R1     = 4.1
		self.R2     = 62.5
		self.CladLeft = 5

		##Resonator Dimentions
		self.Depth  = 40
		self.Width  = 62.5
		self.GAP    = 100
		self.Rw     = 1

		##Src properties
		self.fcen   = 1/1.55
		self.df     = 16
		self.nfreq  = 100

		##MEEP properties
		self.res    = 2
		self.DecayF = 1e-8
		self.WallT  = 0
		self.SimT   = 1e6
		self.today  = str(date.today())
		self.workDir= 'notSet'
		self.filename= 'test'
		self.sim    = None
		self.Objlist = []
		self.Notes   = ''



		#init Data arrays
		self.srcE  = np.array([])
		self.tranE = np.array([])

	def pltModel(self):
		plt.figure(dpi=200)
		self.sim.plot2D(eps_parameters={'alpha':0.8, 'interpolation':'none'})
		

	def mkALLDIRS(self):
		
		self.workingDir = 'data/'+self.today+'/'+self.filename+'/'

		print('WD:',self.workingDir)

		try:
			os.makedirs(self.workingDir)
		except:
			print('AlreadyDir')

		self.sim.use_output_directory(self.workingDir)



	def buildFibre(self):

		self.cell_size = mp.Vector3(400,50,0)
		self.pml_layers = [mp.PML(thickness=4)]

		self.PDMS = mp.Block(
			center=mp.Vector3(0,0,0),
			size=mp.Vector3(mp.inf,mp.inf,mp.inf),
			material=mp.Medium(index=self.PDMSn)
			)

		self.Clad = mp.Block(
			center=mp.Vector3(x=0,y=(-62.5/2 + self.CladLeft),z=0),
			size=mp.Vector3(x=mp.inf,y=62.5,z=mp.inf),
			material=mp.Medium(index=self.cladN)
			)

		self.Core = mp.Block(
			center=mp.Vector3(0,0,0),
			size=mp.Vector3(mp.inf,8.2,mp.inf),
			material=mp.Medium(index=self.coreN)
			)

		self.Objlist.extend([self.PDMS,self.Clad,self.Core])


	def addtriBubbles(self):

		RW = self.Rw
		TL = self.Width

		verts = [
	            
	            mp.Vector3(x=-(RW/2+TL/2) ,y=self.R2 ,z=0)   ,
	            mp.Vector3(x=(RW/2+TL/2)  ,y=self.R2 ,z=0)  ,
	            mp.Vector3(x=(RW/2)       ,y=self.R2-self.Depth ,z=0)   ,
	             mp.Vector3(x=-(RW/2)     ,y=self.R2-self.Depth ,z=0)
	        
	            ]


		self.LH = mp.Prism(center=mp.Vector3(x=-self.GAP/2,y=0,z=0),
	                     vertices = verts,
	                     material=mp.Medium(index=self.PDMSn),
	                     height=1
	                     )

		self.RH = mp.Prism(center=mp.Vector3(x=self.GAP/2,y=0,z=0),
	                     vertices = verts,
	                     material=mp.Medium(index=self.PDMSn),
	                     height=1
	                     )

		self.Objlist.extend([self.LH,self.RH])


	def sqrBubbles(self):

		x=1


	def BuildModel(self):   # builds sim and plots structure to file 
		
		kx = 0.4
		kpoint = mp.Vector3(kx)

		self.src = [
				mp.EigenModeSource(src=mp.GaussianSource(self.fcen,fwidth=self.df),
				center=mp.Vector3(x=-150,y=0),
				size=mp.Vector3(y=20),
				direction=mp.X,
				eig_kpoint=kpoint,
				eig_band=1,
				#eig_parity=mp.EVEN_Y+mp.ODD_Z,
				eig_match_freq=True
				)
			]

		
		self.sim = mp.Simulation(
			geometry_center=mp.Vector3(x=0,y=-5,z=0),
			cell_size=self.cell_size,
			geometry=self.Objlist,
			sources=self.src,
			resolution=self.res,
			force_complex_fields=False,
			eps_averaging=False,
			boundary_layers=self.pml_layers,
			#k_point=mp.Vector3(mp.X)
			)


		self.mkALLDIRS()


		# src flux
		src_fr = mp.FluxRegion(center=mp.Vector3(-190,0,0), size=mp.Vector3(0,20,0))                            
		self.srcE = self.sim.add_flux(self.fcen, 8e-3, 100, src_fr)



		# transmitted flux
		tran_fr = mp.FluxRegion(center=mp.Vector3(190,0,0), size=mp.Vector3(0,20,0))
		self.tranE = self.sim.add_flux(self.fcen, 8e-3, 100, tran_fr)

		plt.figure(dpi=200)
		self.sim.plot2D(eps_parameters={'alpha':0.8, 'interpolation':'none'})
		plt.savefig(self.workingDir+"ModelatStart.pdf")
		#plt.show()


	def RunSetT(self):
		
		t = (1e-6/3e8)
		tFactor = 1e-15/t # converts femptoseconds into unitless MEEP

		print("Actual Simtime:", self.SimT*t)
		
		self.sim.run(
			mp.at_beginning(mp.output_epsilon),
			mp.at_every(10500, mp.output_dpwr),
			until=(self.SimT*tFactor)
			)

		plt.figure(dpi=200)
		self.sim.plot2D(fields=mp.Ez,plot_sources_flag=True,plot_monitors_flag=True)
		plt.savefig(self.workingDir+"FieldsAtEnd.pdf")

		self.meta = {
		"Notes": self.Notes,
        "DecayFactor": self.DecayF,
        "Walltime": self.WallT,
        "Gap": self.GAP,
        "fsrc": self.fcen,
        "df": self.df,
        "nfreq": self.nfreq,
        "resolution": self.res,
        "Depth": self.Depth
        }

		self.dumpData2File()

		fig,axes = plt.subplots(1,1,figsize=(16,9))

		wl = 1/np.array(mp.get_flux_freqs(self.tranE))

		Tran = np.array(mp.get_fluxes(self.tranE))

		Src = np.array(mp.get_fluxes(self.srcE))

		axes.plot(wl,Tran,label='Transmission')
		axes.plot(wl,Src,label='Reflectance')
		#axes.plot(wl,1-Src-Tran,label='Loss')
		axes.legend()
		plt.savefig(self.workingDir+"Spectrum.pdf")

	def dumpData2File(self):
    
		# initialise main data dictionary
		Data = {}
		Data['Src'] = {}       # sensor just after source.
		Data['Out'] = {}       # sensor at the end of the WG (for transmission)
		
		
		Data['Src']['lambda'] = 1/np.array(mp.get_flux_freqs(self.srcE))
		Data['Src']['flux'] = np.array(mp.get_fluxes(self.srcE))
		
		Data['Out']['lambda'] = 1/np.array(mp.get_flux_freqs(self.tranE))
		Data['Out']['flux'] = np.array(mp.get_fluxes(self.tranE))
		

		metadata = {
			"date": str(self.today),
			"Data": self.workingDir+"Data.pk1"
		}

		metadata = {**metadata,**self.meta}
		

		with open(metadata['Data'], 'wb') as file:
			pickle.dump(Data,file)


		with open(self.workingDir + 'metadata.json', 'w') as file:
			json.dump(metadata, file)


