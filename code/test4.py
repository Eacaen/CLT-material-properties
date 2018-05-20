# coding:utf-8
from Fibre_Matrix import Fibre , Matrix
from Lamina import Lamina
from Laminate import Laminate
from Load import Loading
from Failure_Criterion import Failure_Criterion , Puck_Crterion
from laminate_Tools import *

if __name__ == "__main__":
	a = Lamina(69e9 ,6e9 , 3e9 ,v21 = 0.354 ,Xt = 47e6 ,Xc = 14e6,\
				Yt = 24e6 ,Yc = 18e6, S = 75e6,\
				angle = 30,thickness=0.125e-3)

	b = Lamina(69e9 ,6e9 , 3e9 ,v21 = 0.354 ,Xt = 47e6 ,Xc = 14e6,\
				Yt = 24e6 ,Yc = 18e6, S = 75e6,\
				angle = -30,thickness=0.125e-3)

	c = Lamina(69e9 ,6e9 , 3e9 ,v21 = 0.354 ,Xt = 47e6 ,Xc = 14e6,\
				Yt = 24e6 ,Yc = 18e6, S = 75e6,\
				angle = 0,thickness=0.125e-3)
	d = Lamina(69e9 ,6e9 , 3e9 ,v21 = 0.354 ,Xt = 47e6 ,Xc = 14e6,\
				Yt = 24e6 ,Yc  = 18e6, S = 75e6,\
				angle = 90,thickness=0.125e-3)

	LA = Laminate()
	LA.add_Lamina(c)
	LA.add_Lamina(a)
	LA.add_Lamina(b)
	LA.add_Lamina(a)
	LA.add_Lamina(b)
	LA.add_Lamina(d)

	LA.add_Lamina(d)
	LA.add_Lamina(b)
	LA.add_Lamina(a)
	LA.add_Lamina(b)
	LA.add_Lamina(a)
	LA.add_Lamina(c)

	LA.update()


	Load = Loading([30 ,0,0, 0 , 0, 0] )
	Load.apple_to(LA)

	print( Report_stress(Load,mode = '12'))
	print (Report_strain(Load,mode = '12'))
	
	Criterion = Failure_Criterion()

	Criterion.Tsai_Wu(Load)
	print( Criterion.ret_list)
	for lam in LA.lamina_list:
		print(lam.fail_status['Mode'])
 
	Load = Loading([0 ,0,0, 10 , 0, 0] )
	Load.apple_to(LA)
	
	Criterion = Failure_Criterion()

	Criterion.Tsai_Wu(Load)
	print( Criterion.ret_list)
	# plot_stress(Load ,mode = '12',mode2 = '1')

	plot_strain(Load,mode = '12',mode2 = '1')