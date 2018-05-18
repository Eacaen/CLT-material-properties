from laminate_analysis_1 import *
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
	Load = Loading(0 ,0,0, 0 , 10, 0 )
	Load.apple_to(LA)
	print(LA.ABD)
	print( Report_stress(Load,mode = '12'))
	print (Report_strain(Load,mode = '12'))

	criterian = Failure_Criterion()
	criterian.Tsai_Hill(Load)
	ret =  criterian.ret_list
	print( ret)

	# criterian.Tsai_Hill(Load )
	# ret =  criterian.ret_list
	# print '----Tsai_Hill-->',ret

	# criterian.Hoffman(Load )
	# ret =  criterian.ret_list
	# print '----Hoffman-->',ret
	# print Report_stress(Load,layer_num = 11,mode = '12')
	# plot_stress(Load,max_ten = 0,mode = 'xy',mode2 = '1')
	# print Report_strain(Load,mode = '12')
	plot_strain(Load,mode = '12',max_ten = None,mode2 = '1')