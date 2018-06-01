# define lamina by fibre and matrix 

from laminate_analysis_1 import *
	
if __name__ == "__main__":
	f = Fibre(5.4e4,1.8e4,8.8e3,vf21 = 0.25,density = 10 , Xt = 1.05e3,Xc = 1.05e3,\
				Yt = 2.8e1,Yc = 14e1, S = 1.4e1)
	
	m = Matrix(Em = 5.4e4, Gm=8.8e3, vm = 0.25 ,density = 10  ,Xt = 1.05e3,Xc = 1.05e3,\
				Yt = 2.8e1,Yc = 14e1, S = 1.4e1)
	# print b.name_list

	a = Lamina(angle = 0 ,thickness=1 )
	a.Fibre_Matrix_Lamina(fibre = f , matrix = m , fibre_volume = 0.2)
	print( a.matrix_Q)
	print( a.E2)
	print( a.G12)
	print( a.Xc)
	
	a.Chamis_Model(fibre_a = 0.2 , matrix_b = 0.5)
	print( a.E2)
	print( a.G12)