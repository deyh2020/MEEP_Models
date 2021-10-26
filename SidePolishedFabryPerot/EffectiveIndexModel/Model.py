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
		self.Pad = 1

		##Resonator Dimentions / um
		self.Depth  = 40
		self.Width  = 62.5
		self.GAP    = 100

		##Src properties / c=1
		self.fcen   = 1/1.55
		self.df     = 0.1*self.fcen
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
		self.SimSize = 60
		self.PMLThick = 1
		self.SrcSize  = self.SimSize - 2*self.PMLThick
		self.kpoint = mp.Vector3(z=self.fcen*self.coreN)



		#init Data arrays
		self.srcE  = np.array([])
		self.tranE = np.array([])


	def buildFibre(self):

		self.SrcSize  = self.SimSize - 2*self.PMLThick
		self.cell_size = mp.Vector3(self.SimSize,self.SimSize,0)
		self.pml_layers = [
			mp.PML(thickness=self.PMLThick,direction=mp.X),
			mp.PML(thickness=self.PMLThick,direction=mp.Y)
			]

		self.Core = mp.Cylinder(
			radius=self.R1,
			height=mp.inf,
			axis=mp.Vector3(0,0,1),
			material=mp.Medium(index=self.coreN)
			)

		self.Clad = mp.Cylinder(
			radius=self.R2,
			height=mp.inf,
			axis=mp.Vector3(0,0,1),
			material=mp.Medium(index=self.cladN)
			)

		self.Objlist.extend([self.Clad,self.Core])

	def buildPolishedFibre(self):

		self.SrcSize  = self.SimSize - 2*self.PMLThick
		self.cell_size = mp.Vector3(self.SimSize,self.SimSize,0)

		self.pml_layers = [
			mp.PML(thickness=self.PMLThick,direction=mp.X),
			mp.PML(thickness=self.PMLThick,direction=mp.Y)
			]

		self.PolishedZone = mp.Block(
			center=mp.Vector3(y=31.25+4.1+1), 
			size=mp.Vector3(125,62.5,mp.inf), 
			material=mp.Medium(index=1.0))
		

		self.Core = mp.Cylinder(
			radius=self.R1,
			height=mp.inf,
			axis=mp.Vector3(0,0,1),
			material=mp.Medium(index=self.coreN)
			)

		self.Clad = mp.Cylinder(
			radius=self.R2,
			height=mp.inf,
			axis=mp.Vector3(0,0,1),
			material=mp.Medium(index=self.cladN)
			)

		self.Objlist.extend([self.Clad])
		print(self.Objlist)


	def GetEigenModes(self):
		self.sim.init_sim()


		self.EigenmodeData = self.sim.get_eigenmode(
			0.22,
			mp.Z,
			mp.Volume(center=mp.Vector3(),size=mp.Vector3(self.SrcSize,self.SrcSize,0)),
			band_num=1,
			kpoint=self.kpoint,
			match_frequency=False,
			parity=mp.ODD_Y
			)

		fcen = self.EigenmodeData.freq

		print(fcen)

		self.sim.reset_meep()
		self.SrcSize  = self.SimSize - 2*self.PMLThick

		eig_sources = [mp.EigenModeSource(src=mp.GaussianSource(fcen, fwidth=0.1*fcen),
                                      size=mp.Vector3(self.SrcSize,self.SrcSize),
                                      center=mp.Vector3(),
                                      eig_band=1,
                                      eig_kpoint=self.kpoint,
                                      eig_match_freq=False,
                                      eig_parity=mp.ODD_Y)]

		self.sim.change_sources(eig_sources)





	def RunKpoints(self):
		self.sim.init_sim()
		k_interp = 4
		self.sim.run_k_points(2000,mp.interpolate(k_interp,[mp.Vector3(),mp.Vector3(2*0.64516)]))



	def BuildModel(self):   # builds sim and plots structure to file 
		
		
		kpoint = mp.Vector3(z=self.fcen*self.coreN)

		self.src = [
				mp.EigenModeSource(
					src=mp.GaussianSource(
						self.fcen,
						fwidth=self.df
						),
				    center=mp.Vector3(0,0,0),
				    size=mp.Vector3(self.SrcSize,self.SrcSize,0),
				    direction=mp.Z,
				    eig_kpoint=kpoint,
				    eig_band=1,
				    eig_parity=mp.ODD_Y,
				    eig_match_freq=True
				)
			]

		
		self.sim = mp.Simulation(
			cell_size=self.cell_size,
			geometry=self.Objlist,
			sources=self.src,
			resolution=self.res,
			force_complex_fields=True,
			eps_averaging=False,
			boundary_layers=self.pml_layers,
			k_point=kpoint
			)


		self.mkALLDIRS()


		# src flux
		#src_fr = mp.FluxRegion(center=mp.Vector3(-190,0,0), size=mp.Vector3(0,20,0))                            
		#self.srcE = self.sim.add_flux(self.fcen, 8e-3, 100, src_fr)



		# transmitted flux
		#tran_fr = mp.FluxRegion(center=mp.Vector3(190,0,0), size=mp.Vector3(0,20,0))
		#self.tranE = self.sim.add_flux(self.fcen, 8e-3, 100, tran_fr)

		self.pltModel()


	def RunAndPlotF(self):

		t = (1e-6/3e8)
		tFactor = 1e-15/t # converts femptoseconds into unitless MEEP

		print("Actual Simtime:", self.SimT*t)

		self.sim.run(
			#mp.at_beginning(mp.output_epsilon),
			#mp.at_every(10500, mp.output_dpwr),
			#until=(self.SimT*tFactor)
			until_after_sources=self.SimT
			)

		plt.figure(dpi=200)

		self.sim.plot2D(
			output_plane=mp.Volume(center=mp.Vector3(),size=mp.Vector3(self.SimSize,self.SimSize)),
			fields=mp.Ey,
			plot_sources_flag=False,
			plot_monitors_flag=False
			)
		#plt.savefig(self.workingDir+"FieldsAtEnd.pdf")
		plt.show()


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
		self.sim.plot3D(
			fields=mp.Ez,plot_sources_flag=True,plot_monitors_flag=True
			)
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

	def pltModel(self):
		plt.figure(dpi=200)
		self.sim.plot2D(eps_parameters={'alpha':0.8, 'interpolation':'none'})
		plt.show()
		

	def mkALLDIRS(self):
		
		self.workingDir = 'data/'+self.today+'/'+self.filename+'/'

		print('WD:',self.workingDir)

		try:
			os.makedirs(self.workingDir)
		except:
			print('AlreadyDir')

		self.sim.use_output_directory(self.workingDir)

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


