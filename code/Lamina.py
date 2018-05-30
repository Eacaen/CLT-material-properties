# coding:utf-8
from __future__ import print_function
import numpy as np
import scipy as sp
import math
from Fibre_Matrix import Fibre , Matrix
class Lamina(object):
	"""docstring for Lamina"""
	name_counter = 0
	name_list = []
	def __init__(self,E1 = 0, E2 = 0, G12 = 0,v12 = 0,v21 = 0,density=0,\
			Xt = 0, Xc = 0,Yt = 0, Yc = 0, S = 0,max_stain_t = 0,max_stain_c=0,\
			angle = 0,thickness = 0, fibre_volume = 0,\
			fibre=None,matrix=None,name = 'Material_'):
		super(Lamina, self).__init__()
		self.E1 = E1
		self.E2 = E2
		self.G12 = G12

		self.v12 = v12
		self.v21 = v21
		self.density  = density

		self.fail_status =  {"Failed" : False, 
                 			    "Mode" : "" ,
                  			    "Load" : [0]*6 }

		if (self.v21 == 0) and (v12 != 0):
			# print( 'v21 unknown')
			self.v12 = v12
			self.v21 = v12 * self.E1 / self.E2

		if (self.v12 == 0) and (v21 != 0):
			# print( 'v12 unknown')
			self.v21 = v21
			self.v12 = v21 * self.E2 / self.E1

		self.Xt = Xt
		self.Xc = Xc
		self.Yt = Yt
		self.Yc = Yc
		self.S = S
		self.max_stain_t = max_stain_t
		self.max_stain_c = max_stain_c

		self.angle = angle
		self.thickness = thickness

		self.fibre_volume = fibre_volume

		if fibre!=None and matrix!=None:
			raise 'Error, please use function [- Fibre_Matrix_Lamina -]\n'
		elif fibre != None:
			self.fibre = self.Fibre_Matrix_Lamina(fibre,matrix=None,fibre_mass =1 ,fibre_volume = 1)

		elif matrix != None:
			self.matrix = self.Fibre_Matrix_Lamina(matrix=matrix,fibre_mass =0 ,fibre_volume = 0)


		if self.E1 !=0 and self.E2 != 0 and self.G12 !=0 :#or self.fibre!=None or self.matrix!=None: 
			self.update_lamina_matrix()
			

	def properities_degradation(self , pd = 0.001):
	# pd : properities_degradation_parameter for failed layers
		if self.fail_status['Failed'] == True:
			fail_type = self.fail_status['Mode']

			if fail_type == "fiber" or fail_type == "shear":
				self.E1  = self.E1 * pd

				self.E2  = self.E2 * pd
				self.v12 = self.v12 * pd
				self.G12 = self.G12 * pd
				self.v21 = self.v21 
				# self.v21 = self.v12 * self.E2 / self.E1

			elif fail_type == "matrix":
				self.E1  = self.E1
				self.E2  = self.E2 * pd
				self.v12 = self.v12 * pd
				self.G12 = self.G12 * pd
				self.v21 = self.v12 * self.E2 / self.E1

		self.update_lamina_matrix()
		
		self.fail_status['Failed'] = False
			

#************************************************************************
#	get lamina form the fibre and matrix
#	\Phi = fibre_volume  \Psi = fibre_mass
#************************************************************************
	def Fibre_Matrix_Lamina(self,fibre=None,matrix=None,fibre_mass =0 ,fibre_volume = 0, \
						Xt = 0, Xc = 0,Yt = 0, Yc = 0, S = 0,\
						max_stain_t=0,max_stain_c=0):
		if fibre!=None:
			self.fibre = fibre
		else:
			self.fibre = Fibre()

		if matrix!=None:
			self.matrix = matrix
		else:
			self.matrix = Matrix()

		self.fibre_volume = fibre_volume

		fm = fibre_mass   ; mm = 1.0 - fm 

		fv = fibre_volume ; mv = 1.0 - fv

#************************************************************************
#	the E2 from the VDI2014 Part3 p29
#************************************************************************
		self.density = fm * self.fibre.density + mm * self.matrix.density
#************************************************************************
		
#************************************************************************
#	the E2 from the VDI2014 Part3 p29
#************************************************************************
		# a = matrix.Em / (1 - matrix.vm**2)
		# b = 1.0 + 0.85*(fm**2)
		# c = mm**1.25 + (fm*matrix.Em / (fibre.Ef2*(1-matrix.vm**2)))

		# self.E2 =  a *( b / c )
		# self.G12 = matrix.Gm * (1+0.4*(fm**0.5)) / ((mm**1.45) + fm*matrix.Gm/fibre.Gf12)

#************************************************************************
#	the E2 from the eLamX2
##################################################
# Rule of Mixture is a weighted mean approach, provides a quick
# estimation of composite elastic properties.
# • Assumptions
# 1. Fibers are uniformly distributed throughout the matrix.
# 2. Perfect bonding between fibers and matrix.
# 3. Matrix is free of voids.
# 4. Applied loads are either parallel or normal to the fiber direction.
# 5. No residual stresses.
# 6. Fiber and matrix are linearly elastic materials.
##################################################
#************************************************************************						
		if fibre!=None and matrix!=None:
			if Xt== 0 and Xc == 0 and Yt == 0 and Yc == 0 and S == 0:
				self.Xt = self.fibre.Xt * fv + (self.matrix.Em*self.fibre.Xt/self.fibre.Ef1) * mv
				self.Xc = 2.0 * fv*math.sqrt(fv*self.fibre.Ef1*self.matrix.Em)
				# self.Xc = self.matrix.Gm / mv
				self.Yt = self.Xt
#***************************************************************
# the transverse compressive strength is
# about 4-7 times the transverse tensile strength
#***************************************************************
				self.Yc =  self.Yt * 5
				self.S  = 2.0 * (self.fibre.S * fv + self.matrix.S * mv)
			else:
				self.Xt = Xt
				self.Xc = Xc
				self.Yt = Yt
				self.Yc = Yc
				self.S  = S


			self.E1 = self.fibre.Ef1 * fv + self.matrix.Em * mv
			self.E2  = (self.fibre.Ef2 * self.matrix.Em) / (self.matrix.Em * fv + self.fibre.Ef2 * mv )		
			self.G12 = self.fibre.Gf12 * self.matrix.Gm / (self.fibre.Gf12 * mv + self.matrix.Gm * fv)

			self.v12 = self.fibre.vf12 * fv + matrix.vm * mv
			self.v21 = self.v12 * self.E2 / self.E1

		
		elif matrix == None and fibre != None:
			self.Xt = fibre.Xt
			self.Xc = fibre.Xc
			self.Yt = fibre.Yt
			self.Yc = fibre.Yc
			self.S  = fibre.S

			self.E1 = self.fibre.Ef1  
			self.E2  = self.fibre.Ef2
			self.G12 = self.fibre.Gf12 

			self.v21 = self.fibre.vf21 
			self.v12 = self.fibre.vf12  

		elif fibre == None and matrix != None:
			self.Xt = matrix.Xt
			self.Xc = matrix.Xc
			self.Yt = matrix.Yt
			self.Yc = matrix.Yc
			self.S  = matrix.S

			self.E1 = self.matrix.Em  
			self.E2  = self.matrix.Em
			self.G12 = self.matrix.Gm

			self.v21 = self.matrix.vm
			self.v12 = self.matrix.vm 

		self.max_stain_t = max_stain_t
		self.max_stain_c = max_stain_c

		self.update_lamina_matrix()

	def Chamis_Model(self):
		Kf = self.fibre_volume
		Km = 1 - Kf
		self.E1 = self.fibre.Ef1 * Kf + self.matrix.Em * Km
		self.E2 = (1 - math.sqrt(Kf) ) * self.matrix.Em + \
			math.sqrt(Kf)  * self.matrix.Em / (1 - math.sqrt(Kf) *(1 - self.matrix.Em/self.fibre.Ef2) )

		self.G12 = self.matrix.Gm / (1-math.sqrt(Kf) *(1 - self.matrix.Gm/self.fibre.Gf12))
		# self.v12 = (1 - math.sqrt(Kf) ) * self.matrix.vm + math.sqrt(Kf) * self.fibre.vf12  
		self.v12 = self.fibre.vf12 * Kf + self.matrix.vm * Km
		self.v21 = self.v12 * self.E2 / self.E1

		self.Xt = Kf * self.fibre.Xt
		self.Xc = Kf * self.fibre.Xc

		self.Yt = (1 - (math.sqrt(Kf)-Kf)*(1-self.matrix.Em/self.fibre.Ef2))*self.matrix.Xt
		self.Yc = (1 - (math.sqrt(Kf)-Kf)*(1-self.matrix.Em/self.fibre.Ef1))*self.matrix.Xc
		self.S  = (1 - (math.sqrt(Kf)-Kf)*(1-self.matrix.Gm/self.fibre.Gf12))*self.matrix.S


	def update_lamina_matrix(self):
		# self.matrix_S = self.get_S()
		self.matrix_Q = self.get_Q()
		self.matrix_Tstress = self.get_Tstress(self.angle)
		self.matrix_Tstrain = self.get_Tstrain(self.angle)

		if self.angle == 0:
			self.matrix_Q_bar = self.matrix_Q

		if self.angle != 0:
			Tinv = self.matrix_Tstress.I
			self.matrix_Q_bar = ( Tinv * self.matrix_Q ) * (Tinv.T)
		# print( 'lamina define directly , prepare well\n\n')


	def get_S(self):
		matrix_S = np.matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])

		matrix_S[0,0] = 1.0/self.E1
		matrix_S[1,1] = 1.0/self.E2
		matrix_S[2,2] = 1.0/self.G12
		matrix_S[0,1] = -1.0*self.v12 / self.E2
		matrix_S[1,0] = matrix_S[0,1]
		return matrix_S

	def get_Q(self):
		matrix_Q = np.matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])

		matrix_Q[0,0] = self.E1 / (1.0-self.v12*self.v21)
		matrix_Q[1,1] = self.E2 / (1.0-self.v12*self.v21)
		matrix_Q[2,2] = self.G12
		matrix_Q[0,1] = self.v21*self.E2 / (1.0-self.v12*self.v21)
		matrix_Q[1,0] = matrix_Q[0,1]
		return matrix_Q

	def get_Tstress(self,angle):
		"""T transformation matrix between stress_1 = [T] stress_x """ 
		c = np.cos(angle * np.pi/180.0)
		s = np.sin(angle * np.pi/180.0)

		matrix_T = np.matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])

		matrix_T[0,0] = c**2 ; matrix_T[0,1] = s**2 ; matrix_T[0,2] = 2*c*s      ;
		matrix_T[1,0] = s**2 ; matrix_T[1,1] = c**2 ; matrix_T[1,2] = -2*c*s     ;
		matrix_T[2,0] = -1.0*c*s; matrix_T[2,1] = s*c  ; matrix_T[2,2] = c**2 - s**2;
		return matrix_T

	def get_Tstrain(self,angle):
		"""T transformation matrix between strain_1 = [T] strain_x """ 
		c = np.cos(angle*np.pi/180.0)
		s = np.sin(angle*np.pi/180.0)
		matrix_T = np.matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])

		matrix_T[0,0] = c**2 ; matrix_T[0,1] = s**2    ; matrix_T[0,2] = c*s        ;
		matrix_T[1,0] = s**2 ; matrix_T[1,1] = c**2    ; matrix_T[1,2] = -1.0*c*s     ;
		matrix_T[2,0] = -2.0*c*s; matrix_T[2,1] = 2.0*s*c  ; matrix_T[2,2] = c**2 - s**2;
		return matrix_T


if __name__ == "__main__":
	a = Lamina(5.4e4,1.8e4,8.8e3,v21 = 0.25,Xt = 1.05e3,Xc = 1.05e3,\
				Yt = 2.8e1,Yc = 14e1, S = 1.4e1,\
				angle = 0,thickness=1)
	# print a.matrix_Q
	b = Lamina(5.4e4,1.8e4,8.8e3,v21 = 0.25,Xt = 1.05e3,Xc = 1.05e3,\
				Yt = 2.8e1,Yc = 14e1, S = 1.4e1,\
				angle = 90,thickness=10)

	print(a.E1 , a.E2 , a.G12 ,a.v12 , a.v21 , a.angle , a.thickness)	
	print(b.E1 , b.E2 , b.angle , b.thickness)