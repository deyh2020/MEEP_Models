import meep as mp
import numpy as np
import matplotlib.pyplot as plt
import sys, getopt,os
from datetime import date
import pickle,json, os
import time



class Model:

	def __init__(self):

		self.TicToc = self.TicTocGenerator() # create an instance of the TicTocGen generator
		
		##Material N
		self.S      = 1.41
		self.coreN  = 1.445
		self.cladN  = 1.440

		##Fibre Dimentions
		self.R1     = 4.1
		self.R2     = 62.5
		self.Pad    = 0

		##Src properties / c=1
		self.wl     = 1.55
		self.fcen   = 1/self.wl
		self.df     = 2e-2
		self.nfreq  = 1000

		##MEEP properties
		self.res    = 12
		self.DecayF = 1e-8
		self.WallT  = 0
		self.SimT   = 10
		self.today  = str(date.today())
		self.workDir= 'notSet'
		self.filename= 'test'
		self.Datafile = 'Default'
		self.sim    = None
		self.Objlist = []
		self.Notes   = ''
		self.SimSize = 40
		self.PMLThick = 2
		self.SrcSize  = self.SimSize - 2*self.PMLThick
		self.kpoint = mp.Vector3(x=0,y=0,z=self.fcen*self.coreN)

		#LoadTempDependanceData
		self.PDMSindex()
		self.Silicaindex()

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

	def buildPolishedFibre(self,WPDMS=False):

		self.SrcSize  = self.SimSize - 2*self.PMLThick
		self.cell_size = mp.Vector3(self.SimSize,self.SimSize,0)

		self.pml_layers = [
			mp.PML(thickness=self.PMLThick,direction=mp.X),
			mp.PML(thickness=self.PMLThick,direction=mp.Y)
			]

		self.PolishedZone = mp.Block(
			center=mp.Vector3(y=self.R2/2+self.R1+self.Pad), 
			size=mp.Vector3(250,62.5,mp.inf), 
			material=mp.Medium(index=self.nCoating))
		

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

		self.Objlist.extend([self.Clad,self.Core,self.PolishedZone])
		print(self.Objlist)




	def BuildModel(self,Plot=True):   # builds sim and plots structure to file 
		
		self.fcen   = 1/self.wl
		self.df     = 0.1*self.fcen
		self.kpoint = mp.Vector3(x=0,y=0,z=self.fcen*self.coreN)


		self.src = [
				mp.EigenModeSource(
					src=mp.GaussianSource(
						self.fcen,
						fwidth=self.df
						),
				    center=mp.Vector3(0,0,0),
				    size=mp.Vector3(self.SrcSize,self.SrcSize,0),
				    direction=mp.Z,
				    eig_kpoint=self.kpoint,
				    eig_band=1,
				    eig_parity=mp.ODD_Y,
				    eig_match_freq=True,
					eig_resolution=1
				)
			]

		

		
		self.sim = mp.Simulation(
			cell_size=self.cell_size,
			geometry=self.Objlist,
			sources=self.src,
			resolution=self.res,
			symmetries=[mp.Mirror(mp.X)],
			force_complex_fields=True,
			eps_averaging=True,
			boundary_layers=self.pml_layers,
			k_point=self.kpoint,   
			ensure_periodicity=False
			)


		self.mkALLDIRS()


		# src flux
		#src_fr = mp.FluxRegion(center=mp.Vector3(-190,0,0), size=mp.Vector3(0,20,0))                            
		#self.srcE = self.sim.add_flux(self.fcen, 8e-3, 100, src_fr)



		# transmitted flux
		#tran_fr = mp.FluxRegion(center=mp.Vector3(190,0,0), size=mp.Vector3(0,20,0))
		#self.tranE = self.sim.add_flux(self.fcen, 8e-3, 100, tran_fr)
		if Plot:
			self.pltModel()


	def RunMPB(self):

		self.sim.init_sim()
		self.EigenmodeData = self.sim.get_eigenmode(
			self.fcen,
			mp.Z,
			mp.Volume(center=mp.Vector3(),size=mp.Vector3(self.SrcSize,self.SrcSize,0)),
			band_num=1,
			kpoint=self.kpoint,
			match_frequency=True
			)
		self.k = self.EigenmodeData.k
		self.vg = self.EigenmodeData.group_velocity
		self.neff = self.k.norm() * self.wl


	def RunAndPlotF(self):

		t = (1e-6/3e8)
		tFactor = 1e-15/t # converts femptoseconds into unitless MEEP

		print("Actual Simtime:", self.SimT*t)

		self.sim.run(
			until_after_sources=self.SimT
			)

		plt.figure(dpi=200)

		self.sim.plot2D(
			#output_plane=mp.Volume(center=mp.Vector3(),size=mp.Vector3(self.SimSize,self.SimSize)),
			fields=mp.Ey,
			plot_sources_flag=False,
			plot_monitors_flag=False,
			eps_parameters={'alpha':0.8, 'interpolation':'none','cmap':'binary'}
			)
		plt.savefig(self.workingDir+"FieldsAtEnd_"+ str(self.Datafile) +".pdf")
		#plt.show()


	def calcNEFF(self):

		NEFF = (self.wi * self.wl ) / (2 * np.pi * self.gv)
		
		return NEFF


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


	def TicTocGenerator(self):
		# Generator that returns time differences
		ti = 0           # initial time
		tf = time.time() # final time
		while True:
			ti = tf
			tf = time.time()
			yield tf-ti # returns the time difference


	# This will be the main function through which we define both tic() and toc()
	def toc(self,tempBool=True):
		# Prints the time difference yielded by generator instance TicToc
		tempTimeInterval = next(self.TicToc)
		if tempBool:
			print( "Elapsed time: %f seconds.\n" %tempTimeInterval )

	def tic(self):
		# Records a time in TicToc, marks the beginning of a time interval
		self.toc(False)


	def PDMSindex(self):

		self.PDMStemp = np.array([27.04200613, 30.04708872, 40.09978324, 50.0485836, 60.10202556, 70.05194708, 80.00074744])
		self.nPDMS    = np.array([1.410413147,1.409271947,1.405629718,1.4019877,1.398453453,1.394973372,1.391331424])


	def Silicaindex(self):
		
		self.Silicatemp = np.array([22.83686643,40.36719542,70.32692845,103.3346833])
		self.nSilica    = np.array([1.445300107,1.44555516,1.445847903,1.445958546])

	
	def SaveMeta(self):
		
		metadata = {
		##Material N
		"nCoating": self.nCoating,
		"CoreN":self.coreN,
		"CladN":self.cladN,
		
		##Fibre Dimentions
		"R1":self.R1,
		"R2":self.R2,
		"CladLeft":self.Pad,

		##Src properties
		"fcen":self.fcen,
		"df":self.df, 
		"nfreq":self.nfreq,

		##MEEP properties
		#"dpml":self.dpml,
		"resolution":self.res,
		"DecayF":self.DecayF,
		"WallT":self.WallT,
		"SimT":self.SimT,
		"today":self.today,
		"WorkingDir":self.workDir,
		"filename":self.filename,
		"notes":self.Notes,

		"neff":self.neff,

        }

		with open(self.workingDir + 'metadata_' + str(self.Datafile) + '.json' , 'w') as file:
			json.dump(metadata, file)