# coding:utf-8
from Fibre_Matrix import Fibre , Matrix
from Lamina import Lamina
from Laminate import Laminate
from Load import Loading
from Failure_Criterion import Failure_Criterion , Puck_Crterion

if __name__ == "__main__":
	a = Lamina(5.4e10,1.8e7 , 8.8e9,v21 = 0.25,Xt = 1.05e9,Xc = -1.05e9,\
				Yt = 2.8e7,Yc = -14e7, S = 1.4e7,\
				angle = 0,thickness=0.125e-3)
	# print a.matrix_Q
	b = Lamina(5.4e10,1.8e7 , 8.8e9,v21 = 0.25,Xt = 1.05e9,Xc = -1.05e9,\
				Yt = 2.8e7,Yc = -14e7, S = 1.4e7,\
				angle = 90,thickness=0.125e-3)
	# print b.name_list

	LA = Laminate()
	LA.add_Lamina(a)
	LA.add_Lamina(b)
	LA.add_Lamina(a)
	LA.update()
	Force = Loading(0 ,0,0, 0 , 90, 0 )
	Force.apple_to(LA)
	
	print( '\n\n',Force.laminate_stresses_12)

	print("a.fail_status['Mode']" , a.fail_status['Mode'])
	Criterion = Failure_Criterion()

	Criterion.Tsai_Hill(Force,layer_num = None)
	print( Criterion.ret_list)

	Criterion.Tsai_Wu(Force,layer_num = None)
	print( Criterion.ret_list)
	for lam in LA.lamina_list:
		print(lam.fail_status['Mode'])
 
