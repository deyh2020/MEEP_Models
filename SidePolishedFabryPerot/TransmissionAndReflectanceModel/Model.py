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
		self.Rw     = False
		##Src properties
		self.fcen   = 1/1.55
		self.df     = 500
		self.nfreq  = 100

		##MEEP properties
		self.dpml   = 5
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

		self.sx = self.GAP + 2*self.Width + 100 
		self.sy = 100



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



	def buildNormal(self):

			
			
			self.sx = self.GAP + 2*self.Width + 1000 + 2*self.dpml
		
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

		self.sx = self.GAP + 2*self.Width + 500 + 2*self.dpml
		
		self.cell_size = mp.Vector3(self.sx,self.sy,0)

		self.pml_layers = [mp.PML(thickness=self.dpml)]

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


	def sqrBubbles(self,Num):

		RW = self.Rw
		TL = self.Width
		D  = self.Depth

		
		if Num == 1:

			self.Objlist.extend([
				
				mp.Block(
					center=mp.Vector3(x=0,y=-D/2+self.R1+self.CladLeft,z=0),
					size=mp.Vector3(x=TL,y=D,z=mp.inf),
					material=mp.Medium(index=self.PDMSn)
				)
				])

		elif Num == 2:
			self.Objlist.extend([
				
				mp.Block(
					center=mp.Vector3(x=-self.GAP/2,y=-D/2+self.R1+self.CladLeft,z=0),
					size=mp.Vector3(x=TL,y=D,z=mp.inf),
					material=mp.Medium(index=self.PDMSn)
				)
				])
			
			self.Objlist.extend([
				
				mp.Block(
					center=mp.Vector3(x=self.GAP/2,y=-D/2+self.R1+self.CladLeft,z=0),
					size=mp.Vector3(x=TL,y=D,z=mp.inf),
					material=mp.Medium(index=self.PDMSn)
				)
				])



	def BuildModel(self,Plot=False,NormRun=False):   # builds sim and plots structure to file 
		
		kx = 0.4
		kpoint = mp.Vector3(kx)

		self.src = [
				mp.EigenModeSource(src=mp.GaussianSource(self.fcen,fwidth=self.df),
				center=mp.Vector3(x=-(self.sx/2)+5,y=0),
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
			eps_averaging=True,
			boundary_layers=self.pml_layers,
			#k_point=mp.Vector3(mp.X)
			)


		self.mkALLDIRS()


		# src flux
		src_fr = mp.FluxRegion(center=mp.Vector3(-(self.sx/2) + 20,0,0), size=mp.Vector3(0,12,0))                            
		self.refl = self.sim.add_flux(self.fcen, self.df, self.nfreq, src_fr)



		# transmitted flux
		tran_fr = mp.FluxRegion(center=mp.Vector3((self.sx/2) - 5 ,0,0), size=mp.Vector3(0,12,0))
		self.tranE = self.sim.add_flux(self.fcen, self.df, self.nfreq, tran_fr)

		if Plot:
			self.pltModel(Plt=True)
		else:
			self.pltModel(Plt=False)



	def NormRun(self):
		pt = mp.Vector3(0.5*self.sx - 0.5*self.dpml - 1,0)
		print(pt)

		self.sim.run(until_after_sources=mp.stop_when_fields_decayed(2000,mp.Ez,pt,self.DecayF))

		# for normalization run, save flux fields data for reflection plane
		self.norm_refl = self.sim.get_flux_data(self.refl)
		# save incident power for transmission plane
		self.norm_tran = mp.get_fluxes(self.tranE)



	def AutoRun(self):
		
		t = (1e-6/3e8)
		tFactor = 1e-15/t # converts femptoseconds into unitless MEEP

		print("Actual Simtime:", self.SimT*t)


		#pt = mp.Vector3(0.5*self.sx - 0.5*self.dpml - 1,0)
		pt = mp.Vector3(0,0)



		self.sim.run(
			mp.at_beginning(mp.output_epsilon),
			mp.at_every(10500, mp.output_dpwr),
			until_after_sources=mp.stop_when_fields_decayed(2000,mp.Ez,pt,self.DecayF)
			)

		flux_freqs = mp.get_flux_freqs(self.refl)

		refl_flux = mp.get_fluxes(self.refl)
		tran_flux = mp.get_fluxes(self.tranE)

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
		plt.show()



	def SaveMeta(self):
		
		metadata = {
		##Material N
		"PDMS_N": self.PDMSn,
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