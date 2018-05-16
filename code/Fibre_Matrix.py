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