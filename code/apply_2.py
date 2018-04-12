# define lamina by fibre and matrix 

from laminate_analysis_1 import *

if __name__ == "__main__":
	f = Fibre(5.4e4,1.8e4,8.8e3,vf21 = 0.25,density = 10 , Xt = 1.05e3,Xc = 1.05e3,\
				Yt = 2.8e1,Yc = 14e1, S = 1.4e1)
	
	m = Matrix(Em = 5.4e4, Gm=8.8e3, vm = 0.25 ,density = 10  ,Xt = 1.05e3,Xc = 1.05e3,\
				Yt = 2.8e1,Yc = 14e1, S = 1.4e1)
	# print b.name_list

	a = Lamina(fibre=f , angle = 0 ,thickness=1 )
	print( a.matrix_Q)
	b = Lamina(matrix=m, angle = 90,thickness=10.0)

	LA = Laminate()
	LA.add_Lamina(a)
	LA.add_Lamina(b)
	LA.add_Lamina(a)
	LA.update()

	print(a.E1 , a.E2 , a.G12 ,a.v12 , a.v21 , a.angle , a.thickness)	
	# print(b.E1 , b.E2 , b.angle , b.thickness)

	# print(LA.Ex ,LA.Ey )
	# Force = Loading(1,0,0)
	# Force.apple_to(LA)
		
	# print( '\n\n',Force.laminate_stresses_12)

	# Criterion = Failture_Criterion()
	# Criterion.Tsai_Hill(Force,layer_num = None)
	# print( Criterion.ret_list)
