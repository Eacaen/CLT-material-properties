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
	bb = LA.ABD
	print(LA.ABD)
	Force = Loading(10 ,0,0, 0 , 0, 0 )
	Force.apple_to(LA)
	
	print( Report_strain(Force,mode = '12'))

	Criterion = Failure_Criterion()

	Criterion.Tsai_Wu(Force,layer_num = None)
	print( Criterion.ret_list)
	for lam in LA.lamina_list:
		print(lam.fail_status['Mode'])
 
	num = len( LA.lamina_list )
	
	# Holds the analysis data through the loops
	fail_status =  {"Failed?" : [False] * num, 
			"Mode" : [""] * num,
			"Load Factor" : [0] * num}

	failed_count = [0, 0]
	
	# Load factor control
	LF = 0.20	   # Initial load factor
	LS = 1.02	   # Load step multiplier
	
	# Holds results data (in order to plot later)
	plot_data = []

	# Main Load Factor loop (increases when there's no new failure)
	if failed_count[0] < num:

		LA.update()
		for lam in LA.lamina_list:
			print(lam.E1)
		aa = LA.ABD
		print(aa)
		Force = Loading( 100 * LF , 0 , 0 , 0 ,0 , 0 )
		Force.apple_to(LA)

		Criterion = Failure_Criterion()

		Criterion.Tsai_Wu(Force,layer_num = None)
		fail_list = Criterion.ret_list
		print( Criterion.ret_list)


	# 	for i in range(num):
	# 		# print(fail_list[i])
	# 		sf_inf = fail_list[i][0]
	# 		sf_sup = fail_list[i][-1]

	# 		sf = min(fail_list[i])
	# 		# sf = min(sf_inf, sf_sup)
	# 		# print('sf------>  ',sf )

	# 		if sf < 1 and   fail_status["Failed?"][i] == False :
	# 			fail_status["Failed?"][i] = True
	# 			# print('sf------>  ',sf )
	# 			LA.lamina_list[i].fail_status["Failed"] = True
				
	# 			# print('LA.lamina_list[i].E1' , '-', i, LA.lamina_list[i].E1)
	# 			fail_status["Mode"][i] = LA.lamina_list[i].fail_status["Mode"]
	# 			fail_status["Load Factor"][i] = LF
	# 			failed_count[1] = failed_count[1] + 1
	# 			print("Layer "+str(i)+" has failed. Mode: " + LA.lamina_list[i].fail_status["Mode"])

	# 	# Increases LF if no new failure 
	# 	if failed_count[1] == failed_count[0]:	   
	# 		LF = LF*LS		#increases Load Factor by 5%
	# 		# print([int(load) for load in LF*F if load>0])
	# 		print(LF)

	# 	failed_count[0] = failed_count[1]

	# fpf = min(fail_status["Load Factor"])
	# lpf = max(fail_status["Load Factor"])

 #    # Prints results
	# print("First Ply Failure at LF: " + str(round(fpf)))
	# print("Last Ply Failure at LF: " + str(round(lpf)))
	# print("LPF / FPF : " + str(round(lpf/fpf, 1)))