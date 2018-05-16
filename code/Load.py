# coding:utf-8
from __future__ import print_function
import numpy as np
import scipy as sp
import math

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
