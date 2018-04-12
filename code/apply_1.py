# define lamina directly

from laminate_analysis_1 import *

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
	print( a.matrix_Q)
	LA.add_Lamina(b)
	LA.add_Lamina(a)
	LA.update()
	Force = Loading(1,0,0)
	Force.apple_to(LA)
	
	print( '\n\n',Force.laminate_stresses_12)

	Criterion = Failture_Criterion()
	Criterion.Tsai_Hill(Force,layer_num = None)
	print( Criterion.ret_list)
