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
		self.coreN  = 1.445
		self.cladN  = 1.440

		##Fibre Dimentions
		self.R1     = 4.1
		self.R2     = 62.5
		self.CladLeft = 5

		##Resonator Dimentions
		self.Depth  = 40
		self.Width  = 100
		self.GAP    = 100
		self.Rw     = False
		##Src properties
		self.fcen   = 1/1.55
		self.df     = 1.2e-2
		self.nfreq  = 1000

		##MEEP properties
		self.monitorPts = 4
		self.dpml   = 10
		self.res    = 10
		self.DecayF = 1e-6
		self.WallT  = 0
		self.SimT   = 1e6
		self.today  = str(date.today())
		self.workDir= 'notSet'
		self.filename = 'test'
		self.Datafile = 'test'
		self.sim    = None
		self.Objlist = []
		self.Notes   = ''


		#init Data arrays
		self.srcE  = np.array([])
		self.tranE = np.array([])
		

	def mkALLDIRS(self):
		
		self.workingDir = 'data/'+self.today+'/'+self.filename+'/'

		print('WD:',self.workingDir)

		try:
			os.makedirs(self.workingDir)
		except:
			print('AlreadyDir')

		self.sim.use_output_directory(self.workingDir)



	def buildNormalfibre(self):

			self.sx = self.GAP + 2*self.Width + 50 + 2*self.dpml
			self.sy = 2*self.Depth + 2*self.dpml

		
			self.cell_size = mp.Vector3(self.sx,self.sy,0)

			self.pml_layers = [mp.PML(thickness=self.dpml)]


			self.Clad = mp.Block(
				center=mp.Vector3(x=0,y=0,z=0),
				size=mp.Vector3(x=mp.inf,y=62.5,z=mp.inf),
				material=mp.Medium(index=self.cladN)
				)

			self.Core = mp.Block(
				center=mp.Vector3(0,0,0),
				size=mp.Vector3(mp.inf,8.2,mp.inf),
				material=mp.Medium(index=self.coreN)
				)

			self.Objlist.extend([self.Clad,self.Core])

	def buildPolished(self):

		self.sx = self.GAP + 2*self.Width + 2*self.dpml + 100
		self.sy = 2*self.Depth + 2*self.dpml

		
		self.cell_size = mp.Vector3(self.sx,self.sy,0)

		self.pml_layers = [mp.PML(thickness=self.dpml)]

		self.Coating = mp.Block(
			center=mp.Vector3(0,0,0),
			size=mp.Vector3(mp.inf,mp.inf,mp.inf),
			material=mp.Medium(index=self.nCoating)
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

		self.Objlist.extend([self.Coating,self.Clad,self.Core])


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


	def sqrBubbles(self,Num):

		RW = self.Rw
		TL = self.Width
		D  = self.Depth

		
		if Num == 1:

			self.Objlist.extend([
				
				mp.Block(
					center=mp.Vector3(x=0,y=-D/2+self.R1+self.CladLeft,z=0),
					size=mp.Vector3(x=TL,y=D,z=mp.inf),
					material=mp.Medium(index=self.nCoating)
				)
				])

		elif Num == 2:
			self.Objlist.extend([
				
				mp.Block(
					center=mp.Vector3(x=-self.GAP/2-self.Width/2,y=-D/2+self.R1+self.CladLeft,z=0),
					size=mp.Vector3(x=TL,y=D,z=mp.inf),
					material=mp.Medium(index=self.nCoating)
				)
				])
			
			self.Objlist.extend([
				
				mp.Block(
					center=mp.Vector3(x=self.GAP/2+self.Width/2,y=-D/2+self.R1+self.CladLeft,z=0),
					size=mp.Vector3(x=TL,y=D,z=mp.inf),
					material=mp.Medium(index=self.nCoating)
				)
				])



	def BuildModel(self,Plot=False,NormRun=False):   # builds sim and plots structure to file 
		
		kx = 0.4
		kpoint = mp.Vector3(kx)

		self.src = [
				mp.EigenModeSource(src=mp.GaussianSource(self.fcen,fwidth=self.df),
				center=mp.Vector3(x=-(self.sx/2)+2*self.dpml,y=0),
				size=mp.Vector3(y=40),
				direction=mp.X,
				eig_kpoint=kpoint,
				eig_band=1,
				eig_parity=mp.EVEN_Y,
				eig_match_freq=True
				)
			]

		
		self.sim = mp.Simulation(
			#geometry_center=mp.Vector3(x=0,y=-5,z=0),
			cell_size=self.cell_size,
			geometry=self.Objlist,
			sources=self.src,
			resolution=self.res,
			force_complex_fields=False,
			eps_averaging=False,
			boundary_layers=self.pml_layers,
			progress_interval=30
			#k_point=mp.Vector3(mp.X)
			)


		self.mkALLDIRS()


		# src flux
		src_fr = mp.FluxRegion(center=mp.Vector3(-(self.sx/2) + 2*self.dpml+10,0,0), size=mp.Vector3(0,12,0))                            
		self.refl = self.sim.add_flux(self.fcen, self.df, self.nfreq, src_fr)



		# transmitted flux
		tran_fr = mp.FluxRegion(center=mp.Vector3((self.sx/2) - 2*self.dpml ,0,0), size=mp.Vector3(0,12,0))
		self.tranE = self.sim.add_flux(self.fcen, self.df, self.nfreq, tran_fr)

		if NormRun:
			self.sim.plot2D(eps_parameters={'alpha':0.8, 'interpolation':'none'})
			plt.savefig(self.workingDir+"NormModel.pdf")
		else:
			self.sim.plot2D(eps_parameters={'alpha':0.8, 'interpolation':'none'})
			plt.savefig(self.workingDir+"Model.pdf")

		

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
			until=self.sx*self.coreN/0.69
			
			)
		#

		self.sim.run(
		#	#mp.at_beginning(mp.output_epsilon),
		#	#mp.at_every(250,mp.output_efield_z),
			until=mp.stop_when_fields_decayed(
				50,
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

		pt = mp.Vector3()
		self.sim.run(
			mp.at_beginning(mp.output_epsilon),
			mp.at_every(250, mp.output_dpwr),
			until_after_sources=mp.stop_when_fields_decayed(500,mp.Ez,pt,self.DecayF)
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
		plt.savefig(self.workingDir+"TransRef.pdf")
		#plt.show()


	def TimestepFields(self):
		
		fig,axes = plt.subplots(1, 1,dpi=150)

		self.sim.run(
			until=self.SimT
			)
		
		self.sim.plot2D(fields=mp.Ez,plot_sources_flag=True,plot_monitors_flag=True)
		"""
		self.sim.plot2D(
			ax = axes,
			#output_plane=mp.Volume(center=mp.Vector3(),size=mp.Vector3(self.SimSize,self.SimSize)),
			fields=mp.Ez,
			plot_sources_flag=True,
			plot_monitors_flag=True,
			plot_eps_flag=True,
			eps_parameters={'alpha':0.8, 'interpolation':'none','cmap':'binary'}
			)
		"""
		plt.show()


	def SaveMeta(self):
		
		metadata = {
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
		"WorkingDir":self.workDir,
		"filename":self.filename,
		"notes":self.Notes,

		"sx":self.sx,
		"sy":self.sy
        }

		with open(self.workingDir + 'metadata.json', 'w') as file:
			json.dump(metadata, file)




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
		tempTimeInterval = next(self.TicToc)
		if tempBool:
			print( "Elapsed time: %f seconds.\n" %tempTimeInterval )

	def tic(self):
		# Records a time in TicToc, marks the beginning of a time interval
		self.toc(False)



		