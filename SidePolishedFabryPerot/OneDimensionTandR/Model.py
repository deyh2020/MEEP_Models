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
		self.TicToc = self.TicTocGenerator() # create an instance of the TicTocGen generator

		##Material N
		self.nCoating  = 1.41
		self.coreN     = 1.445
		self.cladN     = 1.440

		##Fibre Dimentions
		self.R1     = 4.1
		self.R2     = 62.5
		self.CladLeft = 1

		##Resonator Dimentions
		self.Depth  = 40
		self.Width  = 100
		self.EllipseOffset = 0
		self.GAP    = 0
		self.Rw     = False
		self.BubblesNum = 2 
		self.BubblesType = 'sqr'
		self.FibreType = 'polished'

		##Src properties
		self.fcen   = 1/1.55
		self.df     = 0.8e-2
		self.nfreq  = 1000

		##MEEP properties
		self.dpml   = 10
		self.res    = 10
		self.DecayF = 1e-2
		self.WallT  = 0
		self.SimT   = 1e6
		self.today  = str(date.today())
		self.workingDir= ''
		self.filename = 'test'
		self.Datafile = 'test'
		self.sim    = None
		self.Objlist = []
		self.Notes   = ''
		self.NormComplete = False
		self.SingleNorm = False


		#init Data arrays
		self.srcE  = np.array([])
		self.tranE = np.array([])

		self.PDMSindex()
		self.Silicaindex()

	def RunTRspectrum(self):
		
		self.tic()
		self.Objlist = []							#Reset Model and build structure
		self.buildNormal()  						#builds base polished fibre structure list		
		self.BuildModel(NormRun=True,Plot=True) 

		self.TimestepFields()

		"""

		self.NormRun()
		#Reset sources
		self.sim.reset_meep()
		

		self.Objlist = []	
		self.buildNormal()  						#builds base polished fibre structure list
		self.ADDcircElongated()  					#add sqr bubbles to the structure list
		self.BuildModel(NormRun=False,Plot=True) 

		#load data from the normal run
		self.sim.load_minus_flux_data(self.refl,self.norm_refl)

		self.AutoRun()

		self.toc()

		self.SaveMeta()
		"""

		

	def mkALLDIRS(self):
		
		self.workingDir = 'data/'+self.today+'/'+self.filename+'/'

		print('WD:',self.workingDir)

		try:
			os.makedirs(self.workingDir)
		except:
			print('AlreadyDir')

		self.sim.use_output_directory(self.workingDir)



	def buildNormal(self):

		self.sx = self.Width + 2*self.dpml + 400

		
		self.cell_size = mp.Vector3(self.sx,1,0)

		self.pml_layers = [mp.PML(thickness=self.dpml)]


		self.Coating = mp.Block(
			center=mp.Vector3(0,0,0),
			size=mp.Vector3(mp.inf,mp.inf,mp.inf),
			material=mp.Medium(index=self.nCoating)
			)


		self.Clad = mp.Block(
			center=mp.Vector3(x=0,y=0,z=0),
			size=mp.Vector3(x=mp.inf,y=self.Width,z=mp.inf),
			material=mp.Medium(index=self.cladN)
			)

		self.Objlist.extend([self.Coating,self.Clad])



	def BuildModel(self,Plot=True,NormRun=False):   # builds sim and plots structure to file 
		
		kx = 0.4
		kpoint = mp.Vector3(kx)

		self.src = [
				mp.Source(mp.GaussianSource(self.fcen,fwidth=self.df,is_integrated=True),
                     center=mp.Vector3(x=-(self.sx/2)+2*self.dpml,y=0),
                     component=mp.Ez)
			]

		
		self.sim = mp.Simulation(
			cell_size=self.cell_size,
			geometry=self.Objlist,
			sources=self.src,
			resolution=self.res,
			force_complex_fields=False,
			eps_averaging=False,
			boundary_layers=self.pml_layers,
			progress_interval=30,
			k_point=mp.Vector3(mp.X)
			)


		self.mkALLDIRS()


		# src flux
		src_fr = mp.FluxRegion(center=mp.Vector3(-(self.sx/2) + 2*self.dpml+10,0,0), size=mp.Vector3(0,12,0))                            
		self.refl = self.sim.add_flux(self.fcen, self.df, self.nfreq, src_fr)



		# transmitted flux
		tran_fr = mp.FluxRegion(center=mp.Vector3((self.sx/2) - 2*self.dpml ,0,0), size=mp.Vector3(0,12,0))
		self.tranE = self.sim.add_flux(self.fcen, self.df, self.nfreq, tran_fr)

		
		fig,ax = plt.subplots(dpi=150)
		if NormRun:
			self.sim.plot2D(ax=ax,eps_parameters={'alpha':0.8, 'interpolation':'none'},frequency=0)
			plt.savefig(self.workingDir+"NormModel_" + str(self.Datafile) +".pdf")
		else:
			self.sim.plot2D(ax=ax,eps_parameters={'alpha':0.8, 'interpolation':'none'},frequency=0)
			plt.savefig(self.workingDir+"Model_" + str(self.Datafile) +".pdf")

		if plot == true:
			plt.show()
		

		

	def NormRun(self):

		print("")
		print("")
		print("Normalisation Run")
		print("")
		print("")

		#while sum(mp.get_fluxes(self.tranE)) == 0.0:
		#	print(sum(mp.get_fluxes(self.tranE)))
		#	print("looped")
		
		self.sim.run(
		#	#mp.at_beginning(mp.output_epsilon),
			#mp.at_every(100,mp.output_efield_z),
			until=2*self.sx*self.coreN
			
			)
		#

		self.sim.run(
		#	#mp.at_beginning(mp.output_epsilon),
		#	#mp.at_every(250,mp.output_efield_z),
			until=mp.stop_when_fields_decayed(
				500,
				mp.Ez,mp.Vector3(0.5*self.sx - 0.5*self.dpml,0),self.DecayF
				)
		)

		

		
		# for normalization run, save flux fields data for reflection plane
		self.norm_refl = self.sim.get_flux_data(self.refl)
		# save incident power for transmission plane
		self.norm_tran = mp.get_fluxes(self.tranE)



	def AutoRun(self):
		
		print("")
		print("")
		print("Actual Run")
		print("")
		print("")

		#self.myRunFunction(self.monitorPts)

		self.sim.run(
		#	#mp.at_beginning(mp.output_epsilon),
			#mp.at_every(100,mp.output_efield_z),
			until=self.sx*self.coreN
			
			)

		pt = mp.Vector3(y=-40)

		if self.BubblesNum == 1:
			dt = self.Width
		else:
			dt = self.GAP

		

		self.sim.run(
			#mp.at_beginning(mp.output_epsilon),
			#mp.at_every(500, mp.output_dpwr),
			until_after_sources=mp.stop_when_fields_decayed(dt,mp.Ez,pt,self.DecayF)
			)
		

		flux_freqs = mp.get_flux_freqs(self.refl)
		refl_flux = mp.get_fluxes(self.refl)
		tran_flux = mp.get_fluxes(self.tranE)

		Data = {}
		Data['flux_freqs'] = flux_freqs
		Data['refl_flux'] = refl_flux
		Data['tran_flux'] = tran_flux
		Data['norm_tran'] = self.norm_tran
		Data['norm_refl'] = self.norm_refl

		with open(self.workingDir + self.Datafile + ".pkl", 'wb') as file:
			pickle.dump(Data,file)




		wl = []
		Rs = []
		Ts = []
		for i in range(self.nfreq):
			wl = np.append(wl, 1/flux_freqs[i])
			Rs = np.append(Rs,-refl_flux[i]/self.norm_tran[i])
			Ts = np.append(Ts,tran_flux[i]/self.norm_tran[i])

		plt.figure()
		plt.plot(wl,Rs,'--',label='reflectance')
		plt.plot(wl,Ts,label='transmittance')
		plt.plot(wl,1-Rs-Ts,label='loss')
		#plt.axis([5.0, 10.0, 0, 1])
		plt.xlabel("wavelength (μm)")
		plt.legend(loc="upper right")
		plt.savefig(self.workingDir+"TransRef_" + str(self.Datafile) +".pdf")
		#plt.show()



	def SaveMeta(self):
		
		metadata = {
		"Runtime":self.Runtime,
		"Chunks":self.sim.num_chunks,
		##Material N
		"nCoating": self.nCoating,
		"CoreN":self.coreN,
		"CladN":self.cladN,
		##Fibre Dimentions
		"R1":self.R1,
		"R2":self.R2,
		"CladLeft":self.CladLeft,
		##Resonator Dimentions
		"Depth":self.Depth,
		"Width":self.Width,
		"GAP":self.GAP,
		"Rw":self.Rw,
		##Src properties
		"fcen":self.fcen,
		"df":self.df, 
		"nfreq":self.nfreq,

		##MEEP properties
		"dpml":self.dpml,
		"resolution":self.res,
		"DecayF":self.DecayF,
		"WallT":self.WallT,
		"SimT":self.SimT,
		"today":self.today,
		"WorkingDir":self.workingDir,
		"filename":self.filename,
		"notes":self.Notes,

		"sx":self.sx,
		"sy":self.sy
        }

		
		with open(self.workingDir + str(self.sim.num_chunks) + '_metadata.json', 'w') as file:
			json.dump(metadata, file)




	def dumpData2File(self):
    
		# initialise main data dictionary
		Data = {}
		
		
		Data['Src']['lambda'] = 1/np.array(mp.get_flux_freqs(self.srcE))
		Data['Src']['flux'] = np.array(mp.get_fluxes(self.srcE))
		
		Data['Out']['lambda'] = 1/np.array(mp.get_flux_freqs(self.tranE))
		Data['Out']['flux'] = np.array(mp.get_fluxes(self.tranE))
		

		metadata = {
			"date": str(self.today),
			"Data": self.workingDir+"Data.pk1"
		}

		metadata = {**metadata,**self.meta}
		
		Data = {}
		Data['Src'] = {}       # sensor just after source.
		Data['Out'] = {}       # sensor at the end of the WG (for transmission)

		with open(metadata['Data'], 'wb') as file:
			pickle.dump(Data,file)


		with open(self.workingDir + 'metadata.json', 'w') as file:
			json.dump(metadata, file)


	def pltModel(self,Plt):
		plt.figure(dpi=200)
		self.sim.plot2D(eps_parameters={'alpha':0.8, 'interpolation':'none'})
		if Plt:
			plt.show()
		plt.savefig(self.workingDir+"Model.pdf")


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
		self.Runtime = next(self.TicToc)
		 

	def tic(self):
		self.Runtime = 0
		# Records a time in TicToc, marks the beginning of a time interval
		self.toc(False)

	def PDMSindex(self):

		self.PDMStemp = np.array([27.04200613, 30.04708872, 40.09978324, 50.0485836, 60.10202556, 70.05194708, 80.00074744])
		self.nPDMS    = np.array([1.410413147,1.409271947,1.405629718,1.4019877,1.398453453,1.394973372,1.391331424])
		self.PDMSfit = np.polyfit(self.PDMStemp,self.nPDMS,deg=1)




	def Silicaindex(self):
		
		self.Silicatemp = np.array([22.83686643,40.36719542,70.32692845,103.3346833])
		self.nSilica    = np.array([1.445300107,1.44555516,1.445847903,1.445958546])
		self.SilicaFIT = np.polyfit(self.Silicatemp,self.nSilica,deg=1)