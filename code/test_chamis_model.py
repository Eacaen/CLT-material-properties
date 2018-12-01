# define lamina by fibre and matrix 

from laminate_analysis_1 import *

if __name__ == '__main__':

	thick = 0.00272/12
	fv = 0.4705
	f = Fibre(23e10 ,15e9 , 24e9 ,vf12 = 0.279 ,density = 0 , Xt = 49e8 ,Xc = 441e7 ,\
				Yt = 0  ,Yc = 0 , S = 49e8 )
	
	m = Matrix(Em = 3e9 , Gm= 1.15e9 , vm = 0.3  ,density = 0  ,Xt = 70e6,Xc = 85e6 ,\
				Yt = 0 ,Yc = 0 , S = 45e6 )

	a0 = Lamina(angle = 0 ,thickness= thick )
	a0.Fibre_Matrix_Lamina(fibre = f , matrix = m , fibre_volume = fv)
	a0.Chamis_Model()

	print("a0.E1" ,a0.E1)
	print("a0.E2" ,a0.E2)
	print("a0.G12" ,a0.G12)
	print("a0.v12" ,a0.v12)

	print("a0.Xt" ,a0.Xt)
	print("a0.Xc" ,a0.Xc)
	print("a0.Yt" ,a0.Yt)
	print("a0.Yc" ,a0.Yc)
	print("a0.S" ,a0.S)	
	 

	a45 = Lamina(angle = 45 ,thickness= thick )
	a45.Fibre_Matrix_Lamina(fibre = f , matrix = m , fibre_volume = fv)
	a45.Chamis_Model()	
	print(a45.Xt,a45.Xc,a45.Yt,a45.Yt,a45.S)






# if __name__ == "__main__":

# 	f = Fibre(5.4e4,1.8e4,8.8e3,vf21 = 0.25,density = 10 , Xt = 1.05e3,Xc = 1.05e3,\
# 				Yt = 2.8e1,Yc = 14e1, S = 1.4e1)
	
# 	m = Matrix(Em = 5.4e4, Gm=8.8e3, vm = 0.25 ,density = 10  ,Xt = 1.05e3,Xc = 1.05e3,\
# 				Yt = 2.8e1,Yc = 14e1, S = 1.4e1)
# 	# print b.name_list

# 	a = Lamina(angle = 0 ,thickness=1 )
# 	a.Fibre_Matrix_Lamina(fibre = f , matrix = m , fibre_volume = 0.2)
# 	print( a.matrix_Q)
# 	print( a.E2)
# 	print( a.G12)
# 	print( a.Xc)
	
# 	a.Chamis_Model(fibre_a = 0.2 , matrix_b = 0.5)
# 	print( a.E2)
# 	print( a.G12)