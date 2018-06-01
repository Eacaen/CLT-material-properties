# coding:utf-8
from __future__ import print_function
import numpy as np
import scipy as sp
import math
import copy

class Laminate(object):
	"""docstring for Laminite_"""
	layer_counter = 0
	layer_name_list = []

	def __init__(self,lamina_num = 0,name = 'Layer_' , degradation = 0.001):
		super(Laminate, self).__init__()
		self.lamina_list = []
		self.lamina_num = len(self.lamina_list)
		self.THICK= 0.0
		self.Qk = []   # collect the Q_bar from signal lamina
		self.T_Stress =[]
		self.T_Strain =[]
		self.Zk = []
		self.density = 0
		# self.Zk.append(0.0)   
		#hidden huge bug !!! important !!! read the formula 
		#add in update()
		self.updated = 0
		self.degradation = degradation

		self.A = np.matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])

		self.B = np.matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])

		self.D = np.matrix([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])

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
	def Rule_of_Mixture(self):
		pass



	def update(self):
		if True: #self.updated == 0:
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

		for lamina in self.lamina_list:

			lamina.properities_degradation( self.degradation )
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
		# self.lamina_list.append(lamina)
		self.lamina_list.append(copy.deepcopy(lamina))
		self.updated = 0

	def repalce_Lamina(self,number,lamina):
		del self.lamina_list[number]
		self.lamina_list.insert(number, lamina)
		self.updated = 0

	def remove_Lamina(self,number):
		del self.lamina_list[number]
		self.updated = 0