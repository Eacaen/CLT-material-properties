# coding:utf-8
from __future__ import print_function
import numpy as np
import scipy as sp
import math
#*******************************************************************************
#    	as we can see from the results, the stresses in a signal lamina of 
# 	the loaded-laminate is nearly same among its top,centroid and bottom layer,
# 	so in the strength analysis, only the use the results of the centroid.
#*******************************************************************************

class Failure_Criterion(object):
	"""docstring for Failure_Criterion"""
	def __init__(self):
		super(Failure_Criterion, self).__init__()
		self.ret_list = []
		self.__ret_bottom = 0
		self.__ret_centroid = 0
		self.__ret_top = 0
	
	def Tsai_Hill(self,loading,layer_num = None ):
		self.ret_list = []
		self.__ret_centroid = 0
		 
#************************************************************************
#    Failure_Criterion in the centroid layer
#************************************************************************
		stress_Criterion = loading.laminate_stresses_12

		if layer_num != None:
			stress_ply = stress_Criterion[layer_num*3+1]

			Xt = loading.laminate_loaded.lamina_list[layer_num].Xt
			Xc = loading.laminate_loaded.lamina_list[layer_num].Xc
			Yt = loading.laminate_loaded.lamina_list[layer_num].Yt
			Yc = loading.laminate_loaded.lamina_list[layer_num].Yc
			S  = loading.laminate_loaded.lamina_list[layer_num].S

			sigma_1 = float(stress_ply[0])
			sigma_2 = float(stress_ply[1])
			tau_12  = float(stress_ply[2])
			self.__ret_centroid = (sigma_1 / Xt) **2 - (sigma_1 * sigma_2) / (Xt**2) + \
								(sigma_2 / Yt) **2 + (tau_12 / S) **2
			self.ret_list.append(self.__ret_centroid)

		if layer_num == None:
			a,b,c = np.shape(stress_Criterion)
			for i in range(1,a,3):
				
				layer_num = int((i-1)/3)

				Xt = loading.laminate_loaded.lamina_list[layer_num].Xt
				Xc = loading.laminate_loaded.lamina_list[layer_num].Xc
				Yt = loading.laminate_loaded.lamina_list[layer_num].Yt
				Yc = loading.laminate_loaded.lamina_list[layer_num].Yc
				S  = loading.laminate_loaded.lamina_list[layer_num].S

				stress_ply = stress_Criterion[i]
				sigma_1 = float(stress_ply[0])
				sigma_2 = float(stress_ply[1])
				tau_12  = float(stress_ply[2])

				self.__ret_centroid = (sigma_1 / Xt) **2 - (sigma_1 * sigma_2) / (Xt**2) + \
									(sigma_2 / Yt) **2 + (tau_12 / S) **2
				self.ret_list.append(self.__ret_centroid)


	def Hoffman(self,loading,layer_num = None ):
		self.ret_list = []
		self.__ret_centroid = 0
		 
#************************************************************************
#    Failure_Criterion in the centroid layer
#************************************************************************
		stress_Criterion = loading.laminate_stresses_12

		if layer_num != None:
			stress_ply = stress_Criterion[layer_num*3+1]

			Xt = loading.laminate_loaded.lamina_list[layer_num].Xt
			Xc = loading.laminate_loaded.lamina_list[layer_num].Xc
			Yt = loading.laminate_loaded.lamina_list[layer_num].Yt
			Yc = loading.laminate_loaded.lamina_list[layer_num].Yc
			S  = loading.laminate_loaded.lamina_list[layer_num].S

			sigma_1 = float(stress_ply[0])
			sigma_2 = float(stress_ply[1])
			tau_12  = float(stress_ply[2])
			self.__ret_centroid = (sigma_1 / Xt) **2 - (sigma_1 * sigma_2) / (Xt*Xc) + (sigma_2)**2/(Yt*Yc) +\
								sigma_1 * (Xt - Xc) /(Xt - Xc) - sigma_2 * (Yt * Yc)/(Yt - Yc)+ \
								 	(tau_12 / S) **2
			self.ret_list.append(self.__ret_centroid)

		if layer_num == None:
			a,b,c = np.shape(stress_Criterion)
			for i in range(1,a,3):
				
				layer_num = (i-1)/3.0

				Xt = loading.laminate_loaded.lamina_list[layer_num].Xt
				Xc = loading.laminate_loaded.lamina_list[layer_num].Xc
				Yt = loading.laminate_loaded.lamina_list[layer_num].Yt
				Yc = loading.laminate_loaded.lamina_list[layer_num].Yc
				S  = loading.laminate_loaded.lamina_list[layer_num].S

				stress_ply = stress_Criterion[i]
				sigma_1 = float(stress_ply[0])
				sigma_2 = float(stress_ply[1])
				tau_12  = float(stress_ply[2])

				self.__ret_centroid = (sigma_1 / Xt) **2 - (sigma_1 * sigma_2) / (Xt*Xc) + (sigma_2)**2/(Yt*Yc) +\
								sigma_1 * (Xt - Xc) /(Xt - Xc) - sigma_2 * (Yt * Yc)/(Yt - Yc)+ \
								 	(tau_12 / S) **2
				self.ret_list.append(self.__ret_centroid)



	def Puck(self,loading,layer_num = None ):
		pass

class Puck_Crterion(object):
	"""docstring for Puck_Crterion"""
	def __init__(self):
		super(Puck_Crterion, self).__init__()

		self.ret_list = []
		self.__ret_bottom = 0
		self.__ret_centroid = 0
		self.__ret_top = 0

		self.Pt = 0.30 # P_|_ || tensile
		self.Pc = 0.20  # P_|_ || compressive
		self.Pcc = 0.15 # P_|_ _|_

		self.sigma_11D = 0
	
	def Fibre_Failure(self,loading,layer_num = None ):
		self.ret_list = []
		self.__ret_centroid = 0
		 
#************************************************************************
#    Failure_Criterion in the centroid layer
#************************************************************************
		stress_Criterion = loading.laminate_stresses_12
		strain_Criterion = loading.laminate_strains_12

		if layer_num != None:
			stress_ply = stress_Criterion[layer_num*3+1]
			strain_ply = strain_Criterion[layer_num*3+1]

			sigma_1 = float(stress_ply[0])
			sigma_2 = float(stress_ply[1])
			tau_12  = float(stress_ply[2])

			epsilion_1= float(strain_ply[0])
			gamma_12 = float(strain_ply[2])

			vf12 = loading.laminate_loaded.lamina_list[layer_num].fibre.vf21
			Ef1 = loading.laminate_loaded.lamina_list[layer_num].fibre.Ef1
			max_stain_t = loading.laminate_loaded.lamina_list[layer_num].max_stain_t
			max_stain_c = loading.laminate_loaded.lamina_list[layer_num].max_stain_c


			m = 1.3 #for glass fibre 1.3
	 				#for carbon fibre 1.1
			if (sigma_1 >= 0) and (kk >= 0) and (max_stain_t != 0):
				self.__ret_centroid = 1/max_stain_t*(kk)
				self.ret_list.append(self.__ret_centroid)

			elif sigma_1 < 0 and kk < 0 and (max_stain_t != 0):
				self.__ret_centroid = 1/max_stain_c*abs(kk)+(10*gamma_12)**2
				self.ret_list.append(self.__ret_centroid)
			else:
				self.ret_list.append(None)

		if layer_num == None:
			a,b,c = np.shape(stress_Criterion)
			for i in range(1,a,3):
				
				layer_num = (i-1)/3

				vf12 = loading.laminate_loaded.lamina_list[layer_num].fibre.vf21
				Ef1 = loading.laminate_loaded.lamina_list[layer_num].fibre.Ef1

				max_stain_t = loading.laminate_loaded.lamina_list[layer_num].max_stain_t
				max_stain_c = loading.laminate_loaded.lamina_list[layer_num].max_stain_c

				stress_ply = stress_Criterion[i]
				strain_ply = strain_Criterion[i]

				sigma_1 = float(stress_ply[0])
				sigma_2 = float(stress_ply[1])
				tau_12  = float(stress_ply[2])

				epsilion_1= float(strain_ply[0])
				gamma_12 = float(strain_ply[2])

				m = 1.3 #for glass fibre 1.3#for carbon fibre 1.1
				kk = epsilion_1+vf12*m*sigma_2/Ef1

				if (sigma_1 >= 0) and (kk >= 0) and (max_stain_t != 0):
					self.__ret_centroid = 1/max_stain_t*(kk)
					self.ret_list.append(self.__ret_centroid)

				elif sigma_1 < 0 and kk < 0 and (max_stain_c != 0 ):
					self.__ret_centroid = 1/max_stain_c*abs(kk)+(10*gamma_12)**2
					self.ret_list.append(self.__ret_centroid)
				else:
					self.ret_list.append(None)

	def IFF_Modus_A(self,loading,layer_num = None ):
		self.ret_list = []
		self.__ret_centroid = 0
		 
#************************************************************************
#    Failure_Criterion in the centroid layer
#************************************************************************
		stress_Criterion = loading.laminate_stresses_12
		strain_Criterion = loading.laminate_strains_12

		if layer_num != None:
			stress_ply = stress_Criterion[layer_num*3+1]
			strain_ply = strain_Criterion[layer_num*3+1]

			sigma_1 = float(stress_ply[0])
			sigma_2 = float(stress_ply[1])
			tau_12  = float(stress_ply[2])

			Xt = loading.laminate_loaded.lamina_list[layer_num].Xt
			Xc = loading.laminate_loaded.lamina_list[layer_num].Xc
			Yt = loading.laminate_loaded.lamina_list[layer_num].Yt
			Yc = loading.laminate_loaded.lamina_list[layer_num].Yc
			S  = loading.laminate_loaded.lamina_list[layer_num].S
 
			if sigma_2 > 0:
				a = ( tau_12 /S)**2+(1-self.Pt*Yt/S)**2*(sigma_2/Yt)**2
				b = self.Pt * sigma_2 * 1.0 /S
				c = abs(self.sigma_11D)
				self.__ret_centroid = math.sqrt(a)+b+c
				self.ret_list.append(self.__ret_centroid)
			else:
				self.ret_list.append(None)

		if layer_num == None:
			a,b,c = np.shape(stress_Criterion)
			for i in range(1,a,3):
				
				layer_num = (i-1)/3
	 	
				Xt = loading.laminate_loaded.lamina_list[layer_num].Xt
				Xc = loading.laminate_loaded.lamina_list[layer_num].Xc
				Yt = loading.laminate_loaded.lamina_list[layer_num].Yt
				Yc = loading.laminate_loaded.lamina_list[layer_num].Yc
				S  = loading.laminate_loaded.lamina_list[layer_num].S

				stress_ply = stress_Criterion[i]
				strain_ply = strain_Criterion[i]

				sigma_1 = float(stress_ply[0])
				sigma_2 = float(stress_ply[1])
				tau_12  = float(stress_ply[2])

				if sigma_2 > 0:
					a = ( tau_12 /S)**2+(1-self.Pt*Yt/S)**2*(sigma_2/Yt)**2
					b = self.Pt*sigma_2 * 1.0 /S
					c = abs(self.sigma_11D)

					self.__ret_centroid = math.sqrt(a)+b+c
					self.ret_list.append(self.__ret_centroid)
				else:
					self.ret_list.append(None)

#--------------------------------------------------------------------------------------
	def IFF_Modus_B(self,loading,layer_num = None ):
		self.ret_list = []
		self.__ret_centroid = 0
		 
#************************************************************************
#    Failure_Criterion in the centroid layer
#************************************************************************
		stress_Criterion = loading.laminate_stresses_12
		strain_Criterion = loading.laminate_strains_12

		if layer_num != None:
			stress_ply = stress_Criterion[layer_num*3+1]
			strain_ply = strain_Criterion[layer_num*3+1]

			sigma_1 = float(stress_ply[0])
			sigma_2 = float(stress_ply[1])
			tau_12  = float(stress_ply[2])

			Xt = loading.laminate_loaded.lamina_list[layer_num].Xt
			Xc = loading.laminate_loaded.lamina_list[layer_num].Xc
			Yt = loading.laminate_loaded.lamina_list[layer_num].Yt
			Yc = loading.laminate_loaded.lamina_list[layer_num].Yc
			S  = loading.laminate_loaded.lamina_list[layer_num].S
 			
			Ra = Yc / (2.0 * (1+self.Pcc))
			tau_12c = S * math.sqrt(1+2*self.Pcc)

			if sigma_2 < 0 and (abs(sigma_2 / tau_12) <= Ra / abs(tau_12c)):
				a = (1.0/S) 
				b = self.Pc * sigma_2
				c = abs(self.sigma_11D)

				self.__ret_centroid = a * ( math.sqrt(tau_12**2+b**2) + b ) + c
				self.ret_list.append(self.__ret_centroid)
			else:
				self.ret_list.append(None)

		if layer_num == None:
			a,b,c = np.shape(stress_Criterion)
			for i in range(1,a,3):
				
				layer_num = (i-1)/3
	 	
				Xt = loading.laminate_loaded.lamina_list[layer_num].Xt
				Xc = loading.laminate_loaded.lamina_list[layer_num].Xc
				Yt = loading.laminate_loaded.lamina_list[layer_num].Yt
				Yc = loading.laminate_loaded.lamina_list[layer_num].Yc
				S  = loading.laminate_loaded.lamina_list[layer_num].S

				stress_ply = stress_Criterion[i]
				strain_ply = strain_Criterion[i]

				sigma_1 = float(stress_ply[0])
				sigma_2 = float(stress_ply[1])
				tau_12  = float(stress_ply[2])


				Ra = Yc / (2.0 * (1+self.Pcc))
				tau_12c = S * math.sqrt(1+2*self.Pcc)

				if sigma_2 < 0 and (abs(sigma_2 / tau_12) <= Ra / abs(tau_12c)):
					a = (1.0/S) 
					b = self.Pc*sigma_2
					c = abs(self.sigma_11D)

					self.__ret_centroid = a * ( math.sqrt(tau_12**2+b**2) + b ) +c
					self.ret_list.append(self.__ret_centroid)
				else:
					self.ret_list.append(None)

#--------------------------------------------------------------------------------------
	def IFF_Modus_C(self,loading,layer_num = None ):
		self.ret_list = []
		self.__ret_centroid = 0
		 
#************************************************************************
#    Failure_Criterion in the centroid layer
#************************************************************************
		stress_Criterion = loading.laminate_stresses_12
		strain_Criterion = loading.laminate_strains_12

		if layer_num != None:
			stress_ply = stress_Criterion[layer_num*3+1]
			strain_ply = strain_Criterion[layer_num*3+1]

			sigma_1 = float(stress_ply[0])
			sigma_2 = float(stress_ply[1])
			tau_12  = float(stress_ply[2])

			Xt = loading.laminate_loaded.lamina_list[layer_num].Xt
			Xc = loading.laminate_loaded.lamina_list[layer_num].Xc
			Yt = loading.laminate_loaded.lamina_list[layer_num].Yt
			Yc = loading.laminate_loaded.lamina_list[layer_num].Yc
			S  = loading.laminate_loaded.lamina_list[layer_num].S
 
			Ra = Yc / (2.0 * (1+self.Pcc))
			tau_12c = S * math.sqrt(1+2*self.Pcc)

			if sigma_2 < 0 and (abs(tau_12 / sigma_2 ) <= abs(tau_12c) / Ra):
				a = ( tau_12/( 2.0*(1+self.Pcc)*S) )**2 + (sigma_2/Yc)**2
				b = Yc / (-sigma_2)
				c = abs(self.sigma_11D)

				self.__ret_centroid = a * b + c 

				self.ret_list.append(self.__ret_centroid)
			else:
				self.ret_list.append(None)

		if layer_num == None:
			a,b,c = np.shape(stress_Criterion)
			for i in range(1,a,3):
				
				layer_num = (i-1)/3
	 	
				Xt = loading.laminate_loaded.lamina_list[layer_num].Xt
				Xc = loading.laminate_loaded.lamina_list[layer_num].Xc
				Yt = loading.laminate_loaded.lamina_list[layer_num].Yt
				Yc = loading.laminate_loaded.lamina_list[layer_num].Yc
				S  = loading.laminate_loaded.lamina_list[layer_num].S

				stress_ply = stress_Criterion[i]
				strain_ply = strain_Criterion[i]

				sigma_1 = float(stress_ply[0])
				sigma_2 = float(stress_ply[1])
				tau_12  = float(stress_ply[2])

				Ra = Yc / (2.0 * (1+self.Pcc))
				tau_12c = S * math.sqrt(1+2*self.Pcc)

				if sigma_2 < 0 and (abs(tau_12 / sigma_2 ) <= abs(tau_12c )/ Ra) :
					a = ( tau_12 / (2.0*(1+self.Pcc)*S))**2 + (sigma_2/Yc)**2
					b = Yc / (-sigma_2)
					c = abs(self.sigma_11D)

					self.__ret_centroid = a * b + c 
					
					self.ret_list.append(self.__ret_centroid)
				else:
					self.ret_list.append(None)
