# coding:utf-8
from __future__ import print_function
import numpy as np
import scipy as sp
import math

class Fibre(object):
	"""docstring for Fibre"""
	def __init__(self, Ef1 = 0, Ef2 = 0,Gf12 = 0, vf21 = 0 , vf12 =0 ,density = 0 ,unit = 1, \
		Xt = 0, Xc = 0,Yt = 0, Yc = 0, S = 0,name = 'Fibre_'):
		super(Fibre, self).__init__()

		self.unit = unit
		self.Ef1  = Ef1 * unit
		self.Ef2  = Ef2 * unit
		self.Gf12 = Gf12 * unit
		self.vf21 = vf21 

		if self.Ef1 != 0:
			self.vf12 = self.vf21 * self.Ef2 /  self.Ef1

		self.Xt = Xt
		self.Xc = Xc
		self.Yt = Yt
		self.Yc = Yc
		self.S = S

		self.density  = density
		self.name = name
	def change_Fibre(self, Ef1, Ef2 ,Gf12 ,vf21 ,unit,density,\
			Xt = 0, Xc = 0,Yt = 0, Yc = 0, S = 0,name = 'Fibre_'):
		self.Ef1  = Ef1 * unit
		self.Ef2  = Ef2 * unit
		self.Gf12 = Gf12 * unit
		self.vf21 = vf21

		self.Xt = Xt
		self.Xc = Xc
		self.Yt = Yt
		self.Yc = Yc
		self.S = S

		self.density  = density
		self.name = name

class Matrix(object):
	"""docstring for Matrix"""
	def __init__(self, Em = 0 , Gm = 0, vm = 0 , density = 0,unit =1,\
		Xt = 0, Xc = 0,Yt = 0, Yc = 0, S = 0,name = 'Matrix_'):
		super(Matrix, self).__init__()
		self.Em = Em * unit 
		self.Gm = Gm * unit
		self.vm = vm 
		self.density  = density
		
		self.Xt = Xt
		self.Xc = Xc
		self.Yt = Yt
		self.Yc = Yc
		self.S = S

	def change_Matrix(self, Em ,Gm,vm,unit , density,\
		Xt = 0, Xc = 0,Yt = 0, Yc = 0, S = 0,name = 'Matrix_'):
		self.Em = Em * unit 
		self.Gm = Gm * unit
		self.vm = vm 

		self.Xt = Xt
		self.Xc = Xc
		self.Yt = Yt
		self.Yc = Yc
		self.S = S

		self.density  = density
		self.name = name

class Lamina(object):
	"""docstring for Lamina"""
	name_counter = 0
	name_list = []
	def __init__(self,E1 = 0, E2 = 0, G12 = 0,v12 = 0,v21 = 0,density=0,\
			Xt = 0, Xc = 0,Yt = 0, Yc = 0, S = 0,max_stain_t = 0,max_stain_c=0,\
			angle = 0,thickness = 0,\
			fibre=None,matrix=None,name = 'Material_'):
		super(Lamina, self).__init__()
		self.E1 = E1
		self.E2 = E2
		self.G12 = G12

		self.v12 = v12
		self.v21 = v21
		self.density  = density

		if (self.v21 == 0) and (v12 != 0):
			print( 'v21 unknown')
			self.v12 = v12
			self.v21 = v12 * self.E1 / self.E2

		if (self.v12 == 0) and (v21 != 0):
			print( 'v12 unknown')
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

		if fibre!=None and matrix!=None:
			raise 'Error, please use function [- Fibre_Matrix_Lamina -]\n'
		elif fibre != None:
			self.fibre = self.Fibre_Matrix_Lamina(fibre,matrix=None,fibre_mass =1 ,fibre_volume = 1)

		elif matrix != None:
			self.matrix = self.Fibre_Matrix_Lamina(matrix=matrix,fibre_mass =0 ,fibre_volume = 0)


		if self.E1 !=0 and self.E2 != 0 and self.G12 !=0 or self.fibre!=None or self.matrix!=None: 
			
			self.matrix_S = self.get_S()
			self.matrix_Q = self.get_Q()
			self.matrix_Tstress = self.get_Tstress(self.angle)
			self.matrix_Tstrain = self.get_Tstrain(self.angle)

			if self.angle == 0:
				self.matrix_Q_bar = self.matrix_Q

			if self.angle != 0:
				Tinv = self.matrix_Tstress.I
				self.matrix_Q_bar = ( Tinv * self.matrix_Q ) * (Tinv.T)
			print( 'lamina define directly , prepare well\n\n')
			
		# if name == 'Material_':
		# 	self.name = name + str(len(Lamina.name_list))
		# else :
		# 	self.name = name
		# if self.name:
		# 	Lamina.name_list.append(self.name)
		# 	Lamina.name_counter = Lamina.name_counter + 1

		# def __del__(self):  #if define __del__ , the instance can't delete auto by the system
		# 	n = Lamina.name_list.index(self.name)
		# 	Lamina.name_list.pop(n)
		# 	Lamina.name_counter = Lamina.name_counter - 1
			# print 'Lamina.name_counter',Lamina.name_counter


		def Passion_v(self):
			pass

		def Get_Matrix(self):
			pass	
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
#************************************************************************						
		if fibre!=None and matrix!=None:
			self.Xt = Xt
			self.Xc = Xc
			self.Yt = Yt
			self.Yc = Yc
			self.S  = S

			self.E1 = self.fibre.Ef1 * fm + self.matrix.Em * mm
			self.E2  = (self.fibre.Ef2 * self.matrix.Em) / (self.matrix.Em * fm + self.fibre.Ef2 * mm )		
			self.G12 = self.fibre.Gf12 * self.matrix.Gm / (self.fibre.Gf12 * mm + self.matrix.Gm * fm)

			self.v21 = self.fibre.vf21 * fm + matrix.vm * mm
			self.v12 = self.v21 * self.E2 / self.E1

		
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
		# self.matrix_S = self.get_S()
		# self.matrix_Q = self.get_Q()
		# self.matrix_Tstress = self.get_Tstress(self.angle)
		# self.matrix_Tstrain = self.get_Tstrain(self.angle)

		# if self.angle == 0:
		# 	self.matrix_Q_bar = self.matrix_Q

		# if self.angle != 0:
		# 	Tinv = self.matrix_Tstress.I
		# 	self.matrix_Q_bar = ( Tinv * self.matrix_Q ) * (Tinv.T)

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



class Laminate(object):
	"""docstring for Laminite_"""
	layer_counter = 0
	layer_name_list = []

	def __init__(self,lamina_num = 0,name = 'Layer_'):
		super(Laminate, self).__init__()
		self.lamina_list = []
		self.lamina_num = len(self.lamina_list)
		self.THICK= 0.0
		self.Qk = []   # collect the Q_bar from signal lamina
		self.T_Stress =[]
		self.T_Strain =[]
		self.Zk = []
		self.density = 0
		# self.Zk.append(0.0)     #hidden huge bug !!! important !!! read the formula 
		self.updated = 0

		self.A = np.matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])

		self.B = np.matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])

		self.D = np.matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])



	def update(self):
		if self.updated == 0:
			self.THICK= 0.0
			self.Qk = []   # collect the Q_bar from signal lamina
			self.T_Stress =[]
			self.T_Strain =[]
			self.Zk = []
			self.Zk.append(0.0)     #hidden huge bug !!! important !!! read the formula 
			self.lamina_num = len(self.lamina_list)
			self.density = 0

		self.A = np.matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])

		self.B = np.matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])

		self.D = np.matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])

		for lamina in self.lamina_list[:]:
 			self.Qk.append(lamina.matrix_Q_bar)
 			self.T_Stress.append(lamina.matrix_Tstress)
 			self.T_Strain.append(lamina.matrix_Tstrain)
 			self.THICK = self.THICK + lamina.thickness * 1.0
 			self.Zk.append(self.THICK)# self.Zk.reverse()
 			self.density = self.density + lamina.density * lamina.thickness * 1.0 
		self.density = self.density/self.THICK	
#************************************************************************
#	Get A, B, D Matrix
#   Zk[k] - 1/2 laminate's thickness get the coordinate value of Zk in formula
#	Zk[] is the distance between middle line
#************************************************************************
		for i in range(0,3):
			for j in range(0,3):
				for k in range(0,self.lamina_num):
					qtemp = self.Qk[k]
					self.A[i, j] = self.A[i, j] + (self.Zk[k + 1] - self.Zk [k]) * qtemp[i, j]
					self.B[i, j] = self.B[i, j] + ((self.Zk[k + 1] - (self.THICK)/2) ** 2 - (self.Zk[k] - (self.THICK)/2) ** 2) * qtemp[i, j] / 2.0
					self.D[i, j] = self.D[i, j] + ((self.Zk[k + 1] - (self.THICK)/2) ** 3 - (self.Zk[k] - (self.THICK)/2) ** 3) * qtemp[i, j] / 3.0

 
#************************************************************************
#	**get Astar, Bstar, Cstar, Dstar Matrix
#  ------------------------
#   strain0    A* | B*  N
#   ------ = -------- ---
#	  M        C* | D*  K
#  ------------------------
#************************************************************************
		self.Astar = (self.A).I
		self.Bstar = -1.0*self.Astar * self.B
		self.Cstar = self.B * self.Astar
		self.Dstar = self.D - self.B * self.Astar * self.B

#************************************************************************
#	**get Aprime, Bprime, Cprime, Dprime Matrix
#  ------------------------
#   strain0    A' | B'  N
#   ------- = -------- ---
#	   K       C' | D'  M
#  ------------------------
#************************************************************************
		self.Dprime = (self.Dstar).I
		self.Aprime = self.Astar - self.Bstar * self.Dprime * self.Cstar
		self.Bprime = self.Bstar * self.Dprime
		self.Cprime = self.Bprime.T


		self.ABD = np.bmat([[self.A,self.B],[self.B,self.D]])
		self.abd = (self.ABD).I
		self.detABD = np.linalg.det(self.ABD)
############################################################################
# get the effective  Young's moduli
############################################################################	
		Axx = np.matrix([[self.A[1,1],self.A[1,2]],\
						[self.A[1,2],self.A[2,2]]])

		Bxx = np.matrix([[self.B[0,1], self.B[1,1], self.B[1,2]],\
						[self.B[0,2], self.B[1,2], self.B[2,2]]])

		effective_Exx = np.bmat([[Axx,Bxx],[Bxx.T,self.D]])

		self.Ex = self.detABD/(np.linalg.det(effective_Exx) * self.THICK)
 
#--------------------------------------------------------------------------------

		Axx = np.matrix([[self.A[0,0], self.A[0,2]],\
						[self.A[0,2], self.A[2,2]]])

		Bxx = np.matrix([[self.B[0,0], self.B[0,1], self.B[0,2]],\
						[self.B[0,2], self.B[1,2], self.B[2,2]]])

		effective_Eyy = np.bmat([[Axx,Bxx],[Bxx.T,self.D]])

		self.Ey = self.detABD/(np.linalg.det(effective_Eyy) * self.THICK)

#--------------------------------------------------------------------------------

		# Axx = np.matrix([[self.A[0,0], self.A[0,1]],\
		# 				[self.A[0,1], self.A[1,1]]])

		# Bxx = np.matrix([[self.B[0,0], self.B[0,1], self.B[0,2]],\
		# 				[self.B[0,1], self.B[1,1], self.B[1,2]]])

		# effective_Gxy = np.bmat([[Axx,Bxx],[Bxx.T,self.D]])
		effective_Gxy=\
		np.matrix([
				[self.A[0,0], self.A[0,1], self.B[0,0], self.B[0,1], self.B[0,2]],
				[self.A[0,1], self.A[1,1], self.B[0,1], self.B[1,1], self.B[1,2]],
				[self.B[0,0], self.B[0,1], self.D[0,0], self.D[0,1], self.D[0,2]],
				[self.B[0,1], self.B[1,1], self.D[0,1], self.D[1,1], self.D[1,2]],
				[self.B[0,2], self.B[1,2], self.D[0,2], self.D[1,2], self.D[2,2]]
				])

		self.Gxy = self.detABD/(np.linalg.det(effective_Gxy) * self.THICK)
		self.G = self.Gxy 
#--------------------------------------------------------------------------------
# 	  - Epison_y
#  Vxy = ------------
#	   Epison_x
#--------------------------------------------------------------------------------
		Axx = np.matrix([[self.A[0,1], self.A[1,2]],\
						[self.A[0,2], self.A[2,2]]])

		Bxx = np.matrix([[self.B[0,1], self.B[1,1], self.B[1,2]],\
						[self.B[0,2], self.B[1,2], self.B[2,2]]])

		Bxx2 = np.matrix([[self.B[0,0], self.B[0,1], self.B[0,2]],\
						[self.B[0,2], self.B[1,2], self.B[2,2]]])

		effective_Vxy = np.bmat([[Axx,Bxx],[Bxx2.T,self.D]])

		self.Vxy = -1 * np.linalg.det(effective_Vxy) / np.linalg.det(effective_Exx)

#--------------------------------------------------------------------------------
# 		  - Epison_y
#  Vyx = ------------
#		   Epison_x
#--------------------------------------------------------------------------------
		Axx = np.matrix([[self.A[0,1], self.A[1,2]],\
						[self.A[0,2], self.A[2,2]]])

		Bxx = np.matrix([[self.B[0,0], self.B[0,1], self.B[0,2]],\
						[self.B[0,2], self.B[1,2], self.B[2,2]]])

		effective_Vyx = np.bmat([[Axx,Bxx],[Bxx.T,self.D]])


		Axxy = np.matrix([[self.A[0,0], self.A[0,2]],\
						[self.A[0,2], self.A[2,2]]])

		Bxxy = np.matrix([[self.B[0,1], self.B[1,1], self.B[1,2]],\
						[self.B[0,2], self.B[1,2], self.B[2,2]]])

		effective_Vyxy = np.bmat([[Axxy,Bxxy],[Bxxy.T,self.D]])

		self.Vyx = -1 * np.linalg.det(effective_Vyx) / np.linalg.det(effective_Vyxy)

#--------------------------------------------------------------------------------

		self.updated = 1      

	def add_Lamina(self,lamina):
		self.lamina_list.append(lamina)
		self.updated = 0

	def repalce_Lamina(self,number,lamina):
		del self.lamina_list[number]
		self.lamina_list.insert(number, lamina)
		self.updated = 0

	def remove_Lamina(self,number):
		del self.lamina_list[number]
		self.updated = 0


class Loading(object):
	"""docstring for Loading"""
	def __init__(self, Nx = 0 , Ny = 0, Nxy = 0,Mx = 0,My = 0,Mxy = 0):
		super(Loading, self).__init__()
		self.Nx = Nx ; self.Ny = Ny ; self.Nxy = Nxy
		self.Mx = Mx ; self.My = My ; self.Mxy = Mxy
		self.load = np.zeros((6,1),dtype = np.float64)

		self.load[0] = float(Nx)
		self.load[1] = float(Ny)
		self.load[2] = float(Nxy)
		self.load[3] = float(Mx)
		self.load[4] = float(My)
		self.load[5] = float(Mxy)

		# self.laminate_loaded = 0
		self.laminate_loaded = self #need check!!!!!!!!

		self.laminate_stresses_12 = []
		self.laminate_strains_12 = []

		self.laminate_stresses_xy = []
		self.laminate_strains_xy = []

	def apple_to(self,laminate):
		self.laminate_stresses_12 = []
		self.laminate_strains_12 = []

		self.laminate_stresses_xy = []
		self.laminate_strains_xy = []
#************************************************************************		
		self.laminate_loaded = laminate

#************************************************************************
#    Strains and Curvatures in the mid-plane
#************************************************************************
		self.epsilon_k = self.laminate_loaded.abd * self.load
		
		self.epsilon_x0  = self.epsilon_k[0]
		self.epsilon_y0  = self.epsilon_k[1]
		self.epsilon_z0  = self.epsilon_k[2]
		self.epsilon_kx0 = self.epsilon_k[3]
		self.epsilon_ky0 = self.epsilon_k[4]
		self.epsilon_kz0 = self.epsilon_k[5]

		for k in range(0,laminate.lamina_num):

#************************************************************************
#    Strains and Curvatures in the k laminate's top
#************************************************************************
			coor_z = self.laminate_loaded.Zk[k] - self.laminate_loaded.THICK/2.0

			strain_kxy = self.epsilon_k[0:3] + coor_z * self.epsilon_k[3:6]
			stresses_kxy = self.laminate_loaded.Qk[k] * strain_kxy

			strain_k12 = self.laminate_loaded.T_Strain[k] * strain_kxy
			stresses_k12 = self.laminate_loaded.T_Stress[k] * stresses_kxy

			self.laminate_stresses_xy.append(stresses_kxy)
			self.laminate_strains_xy.append(strain_kxy)

			self.laminate_stresses_12.append(stresses_k12)
			self.laminate_strains_12.append(strain_k12)
		
			
#************************************************************************
#    Strains and Curvatures in the k laminate's centroid
#************************************************************************
			coor_z = (self.laminate_loaded.Zk[k+1] + self.laminate_loaded.Zk[k])/2.0 - \
					self.laminate_loaded.THICK/2.0

			strain_kxy = self.epsilon_k[0:3] + coor_z * self.epsilon_k[3:6]
			stresses_kxy = self.laminate_loaded.Qk[k] * strain_kxy

			strain_k12 = self.laminate_loaded.T_Strain[k] * strain_kxy
			stresses_k12 = self.laminate_loaded.T_Stress[k] * stresses_kxy

			self.laminate_stresses_xy.append(stresses_kxy)
			self.laminate_strains_xy.append(strain_kxy)

			self.laminate_stresses_12.append(stresses_k12)
			self.laminate_strains_12.append(strain_k12)
		

#************************************************************************
#    Strains and Curvatures in the k laminate's bottom
#************************************************************************
			coor_z = self.laminate_loaded.Zk[k+1] - self.laminate_loaded.THICK/2.0

			strain_kxy = self.epsilon_k[0:3] + coor_z * self.epsilon_k[3:6]
			stresses_kxy = self.laminate_loaded.Qk[k] * strain_kxy

			strain_k12 = self.laminate_loaded.T_Strain[k] * strain_kxy
			stresses_k12 = self.laminate_loaded.T_Stress[k] * stresses_kxy

			self.laminate_stresses_xy.append(stresses_kxy)
			self.laminate_strains_xy.append(strain_kxy)

			self.laminate_stresses_12.append(stresses_k12)
			self.laminate_strains_12.append(strain_k12)


	def change_Load(self, Nx = 0 , Ny = 0, Nxy = 0,Mx = 0,My = 0,Mxy = 0):
		self.load = np.zeros((6,1),dtype = np.float64)
		self.Nx = Nx ; self.Ny = Ny ; self.Nxy = Nxy
		self.Mx = Mx ; self.My = My ; self.Mxy = Mxy
		self.load[0] = float(Nx)
		self.load[1] = float(Ny)
		self.load[2] = float(Nxy)
		self.load[3] = float(Mx)
		self.load[4] = float(My)
		self.load[5] = float(Mxy)

#*******************************************************************************
#    	as we can see from the results, the stresses in a signal lamina of 
# 	the loaded-laminate is nearly same among its top,centroid and bottom layer,
# 	so in the strength analysis, only the use the results of the centroid.
#*******************************************************************************

class Failture_Criterion(object):
	"""docstring for Failture_Criterion"""
	def __init__(self):
		super(Failture_Criterion, self).__init__()
		self.ret_list = []
		self.__ret_bottom = 0
		self.__ret_centroid = 0
		self.__ret_top = 0
	
	def Tsai_Hill(self,loading,layer_num = None ):
		self.ret_list = []
		self.__ret_centroid = 0
		 
#************************************************************************
#    Failture_Criterion in the centroid layer
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
#    Failture_Criterion in the centroid layer
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
#    Failture_Criterion in the centroid layer
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
#    Failture_Criterion in the centroid layer
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
#    Failture_Criterion in the centroid layer
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
#    Failture_Criterion in the centroid layer
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

#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------	
if __name__ == "__main__":
	a = Lamina(5.4e4,1.8e4,8.8e3,v21 = 0.25,Xt = 1.05e3,Xc = 1.05e3,\
				Yt = 2.8e1,Yc = 14e1, S = 1.4e1,\
				angle = 0,thickness=1)
	# print a.matrix_Q
	b = Lamina(5.4e4,1.8e4,8.8e3,v21 = 0.25,Xt = 1.05e3,Xc = 1.05e3,\
				Yt = 2.8e1,Yc = 14e1, S = 1.4e1,\
				angle = 90,thickness=10)
	# print b.name_list

	LA = Laminate()
	LA.add_Lamina(a)
	LA.add_Lamina(b)
	LA.add_Lamina(a)
	LA.update()
	Force = Loading(1,0,0)
	Force.apple_to(LA)
	
	print( '\n\n',Force.laminate_stresses_12)

	Criterion = Failture_Criterion()
	Criterion.Tsai_Hill(Force,layer_num = None)
	print( Criterion.ret_list)



