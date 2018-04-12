# coding:utf-8
# ////////////////////////////////////////////////////////////////////
# //                          _ooOoo_                               //
# //                         o8888888o                              //
# //                         88" . "88                              //
# //                         (| ^_^ |)                              //
# //                         O\  =  /O                              //
# //                      ____/`---'\____                           //
# //                    .'  \\|     |//  `.                         //
# //                   /  \\|||  :  |||//  \                        //
# //                  /  _||||| -:- |||||-  \                       //
# //                  |   | \\\  -  /// |   |                       //
# //                  | \_|  ''\---/''  |   |                       //
# //                  \  .-\__  `-`  ___/-. /                       //
# //                ___`. .'  /--.--\  `. . ___                     //
# //              ."" '<  `.___\_<|>_/___.'  >'"".                  //
# //            | | :  `- \`.;`\ _ /`;.`/ - ` : | |                 //
# //            \  \ `-.   \_ __\ /__ _/   .-` /  /                 //
# //      ========`-.____`-.___\_____/___.-`____.-'========         //
# //                           `=---='                              //
# //      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^        //
# //              佛祖保佑                永无BUG                     //
# //             Buddha bless            BUG away                   //
# ////////////////////////////////////////////////////////////////////

from laminate_analysis_1 import *
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from collections import OrderedDict
def where_dot(ddoo):
	i = 0
	if isinstance(ddoo,int):
		return
	while abs(ddoo)<1:
		ddoo = ddoo * 10
		i = i + 1
	return i

def Report_stress(Load,layer_num = None,mode = '12',save = ''):
	mode = str(mode)
	# stress = {}  #the directory has no order when push key and value in it
	stress = OrderedDict()
	layer = []
	
	if mode == '12':
		stress_report = Load.laminate_stresses_12
	elif  mode == 'xy':
		stress_report = Load.laminate_stresses_xy
	else:
		print 'mode_error'
		return 

	if layer_num == None:
		
		a,b,c = np.shape(stress_report)
		# print a,b,c
		for j in range(0,a/3):
			for i in range(0,3):
				if i == 0:
					s = 'Layer_' + str(j) + '_top'
					layer.append(s)
				if i == 1:
					s = 'Layer_' + str(j) + '_centroid'
					layer.append(s)
				if i == 2:
					s = 'Layer_' + str(j) + '_bottom'
					layer.append(s)	

		for i in range(0,a):
			x1 = float(stress_report[i][0])
			x2 = float(stress_report[i][1])
			x3 = float(stress_report[i][2])
			stress[layer[i]] = [x1,x2,x3]


	if layer_num != None:
		layer_num = int(layer_num)
		stress_layer = stress_report[ layer_num*3 : layer_num*3+3]
		s = 'Layer_' + str(layer_num) + '_top'
		layer.append(s)
		s = 'Layer_' + str(layer_num) + '_centroid'
		layer.append(s)
		s = 'Layer_' + str(layer_num) + '_bottom'
		layer.append(s)

		for i in range(0,3):
			x1 = float(stress_layer[i][0])
			x2 = float(stress_layer[i][1])
			x3 = float(stress_layer[i][2])
			stress[layer[i]] = [x1,x2,x3]
			

	frame = pd.DataFrame(stress)
	if mode == '12':
		frame.index = ['sigma_1','sigma_2','tau_12']
	elif  mode == 'xy':
		frame.index = ['sigma_x','sigma_y','tau_xy']

	frame = frame.T
	if save:
		import string
		save = str(save).split('.')[0]
		frame.to_excel(save + '.xlsx')
	return frame

def Report_strain(Load,layer_num = None,mode = '12',save = ''):
	strain = OrderedDict()
	layer = []

	if mode == '12':
		strain_report = Load.laminate_strains_12
	elif  mode == 'xy':
		strain_report = Load.laminate_strains_xy
	else:
		print 'mode_error'
		return 

	if layer_num == None:
		
		a,b,c = np.shape(strain_report)
		for j in range(0,a/3): #a/3 = number of lamina
			for i in range(0,3):
				if i%3 == 0:
					s = 'Layer_' + str(j) + '_top'
					layer.append(s)
				if i%3 == 1:
					s = 'Layer_' + str(j) + '_centroid'
					layer.append(s)
				if i%3 == 2:
					s = 'Layer_' + str(j) + '_bottom'
					layer.append(s)	

		for i in range(0,a):
			x1 = float(strain_report[i][0])
			x2 = float(strain_report[i][1])
			x3 = float(strain_report[i][2])
			strain[layer[i]] = [x1,x2,x3]


	if layer_num != None:
		layer_num = int(layer_num)
		strain_layer = strain_report[layer_num*3:layer_num*3+3]

		s = 'Layer_' + str(layer_num) + '_top'
		layer.append(s)
		s = 'Layer_' + str(layer_num) + '_centroid'
		layer.append(s)
		s = 'Layer_' + str(layer_num) + '_bottom'
		layer.append(s)

		for i in range(0,3):
			x1 = float(strain_layer[i][0])
			x2 = float(strain_layer[i][1])
			x3 = float(strain_layer[i][2])
			strain[layer[i]] = [x1,x2,x3]

	frame = pd.DataFrame(strain)
	if mode == '12':
		frame.index = ['epsilon_1','epsilon_2','gamma_12']
	elif  mode == 'xy':
		frame.index = ['epsilon_x','epsilon_y','gamma_xy']

	frame = frame.T
	if save:
		import string
		save = str(save).split('.')[0]
		frame.to_excel(save + '.xlsx')
	return frame

def plot_stress(Load,layer_num = None,max_ten = None,max_com = None,\
				mode = '12',mode2 = 'x',save = ''):
	'''
	max_ten means max tensile
	'''
	mode = str(mode)
	mode2 = str(mode2)

	if mode == '12':
		stress_plot = Load.laminate_stresses_12
	elif  mode == 'xy':
		stress_plot = Load.laminate_stresses_xy
	else:
		print 'mode_error'
		return 

   	fig = plt.figure()
	ax1 = fig.add_subplot(111)
#-----------------------------------------------------------
	if mode2 == '1':
		show_num = 0
		ax1.set_xlabel(r'$\sigma_1$',size = 18)
	elif mode2 == 'x':
		show_num = 0
		ax1.set_xlabel(r'$\sigma_x$',size = 18)
#-----------------------------------------------------------
	elif mode2 == '2':
		show_num = 1
		ax1.set_xlabel(r'$\sigma_2$',size = 18)
	elif mode2 == 'y':
		show_num = 1
		ax1.set_xlabel(r'$\sigma_y$',size = 18)
#-----------------------------------------------------------
	elif mode2 == 'z' or mode2 == 'xy':
		show_num = 2
		ax1.set_xlabel(r'$\sigma_{xy}$',size = 18)

	elif mode2 == '3' or mode2 == '12':
		show_num = 2
		ax1.set_xlabel(r'$\sigma_{12}$',size = 18)	
#-----------------------------------------------------------
	else:
		print 'should choose a right stress to plot'
		return

	if layer_num == None:
		y = Load.laminate_loaded.Zk
#************************************************************************
#	get the z coordinate value
#************************************************************************
		thk = Load.laminate_loaded.THICK / 2.0
		y_list = [x - thk for x in y]
#************************************************************************
#	push the top/bottom top/bottom into the list
#************************************************************************
		a,b,c = np.shape(stress_plot)
		sp = []
		for j in range(0,a/3): #a/3 = number of lamina
			sp.append(float(stress_plot[j*3][show_num]))  # choose which to plot
			sp.append(float(stress_plot[j*3+2][show_num]))
			#push the lamina's top and bottom in the list as their order in laminate
#************************************************************************
#	data solution , expand the middle part of data
#   eg. [-10 -3 3 10] to [-10 -3 -3 3 3 10]
#************************************************************************
		yy = []
		yy.append(y_list[0])
		for i in range(1,len(y_list)-1):
			yy.append(y_list[i])
			yy.append(y_list[i])
		yy.append(y_list[-1])
#************************************************************************
#	add the straight line to divide the lamina
#************************************************************************
  		for i in range(0,len(yy)/2 ):
  			straigh_x = np.linspace(abs(sp[2*i])/10.0 , sp[2*i])
  			straigh_y = [n*yy[2*i] for n in np.ones(len(straigh_x))]
			ax1.plot(straigh_x,straigh_y,'--')

		straigh_x = np.linspace(abs(sp[len(yy)-1])/10.0 , sp[len(yy)-1])
  		straigh_y = [n*yy[len(yy)-1] for n in np.ones(len(straigh_x))]
		ax1.plot(straigh_x,straigh_y,'--')


#************************************************************************
#	set y axis range
#************************************************************************
		ax1.set_ylabel('Z(k)')
		ax1.set_ylim(y_list[0],y_list[-1])
		plt.plot(sp,yy,'black')
		# print sp,yy

		# for i in range(len(sp)-1):
		# 	plt.fill_between([sp[i],sp[i+1] ],yy[i],yy[i+1], alpha=0.3)
#************************************************************************
#	move the x or y axis to the origin position
#************************************************************************		ax1.yaxis.set_ticks_position('left')
		ax1.spines['left'].set_position(('data', 0))
		# ax1.xaxis.set_ticks_position('bottom')
		# ax1.spines['bottom'].set_position(('data', 0))

#************************************************************************
#	add the max_criterion straight in the figure
#************************************************************************
		if max_ten != None:
			
			max_y = np.linspace(y_list[0], y_list[-1],10)
			# range(int(y_list[0]),int(y_list[-1] + 1))
			max_x = [n*max_ten for n in np.ones(len(max_y))]
			plt.annotate('max tensile',xy=(max_ten,0),xytext=(max_ten+1,0))
					# ,arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
			ax1.plot(max_x,max_y,'red')

		if max_com != None:
			max_y = np.linspace(y_list[0], y_list[-1],10)
			max_x = [n*max_com for n in np.ones(len(max_y))]
			plt.annotate('max compressive',xy=(max_com,0),xytext=(max_com,0))
			ax1.plot(max_x,max_y,'red')
#************************************************************************
#	set title , plot figure
#************************************************************************
		fig.suptitle('stress distribution in lamina')
		plt.grid()
		plt.show()


def plot_strain(Load,layer_num = None,max_ten = None,max_com = None,\
				mode = '12',mode2 = 'x',save = ''):
	mode = str(mode)
	mode2 = str(mode2)

	if mode == '12':
		strain_plot = Load.laminate_strains_12
	elif  mode == 'xy':
		strain_plot = Load.laminate_strains_xy
	else:
		print 'mode_error'
		return
	fig = plt.figure()
	ax1 = fig.add_subplot(111)

	if mode2 == 'x' or mode2 == '1':
		show_num = 0
		x_str1 = r'$\epsilon_1$'

	elif mode2 == 'y' or mode2 == '2':
		show_num = 1
		x_str1 = r'$\epsilon_2$' 

	elif mode2 == 'z' or mode2 == 'xy':
		show_num = 2
		x_str1 = r'$\epsilon_{xy}$' 

	elif mode2 == '3' or mode2 == '12':
		show_num = 2
		x_str1 = r'$\epsilon_{12}$' 	
	else:
		print 'should choose a right strain to plot'
		return
   
      
	if layer_num == None:
		y = Load.laminate_loaded.Zk
		thk = Load.laminate_loaded.THICK / 2.0
		y_list = [x - thk for x in y]
		a,b,c = np.shape(strain_plot)
		sp = []
		for j in range(0,a/3): #a/3 = number of lamina
			sp.append(float(strain_plot[j*3][show_num]))  # choose which to plot
			sp.append(float(strain_plot[j*3+2][show_num]))
			#push the lamina's top and bottom in the list as their order in laminate
#************************************************************************
#	the strains's value maybe to small to plot
#   times by a number and make them become integer
#************************************************************************		
		dots = where_dot(min(sp))
		sp = [n*10**dots for n in sp]

		yy = []
		yy.append(y_list[0])
		for i in range(1,len(y_list)-1):
			yy.append(y_list[i])
			yy.append(y_list[i])
		yy.append(y_list[-1])
  		
  		for i in range(0,len(yy)/2 ):
  			straigh_x = np.linspace(abs(sp[2*i])/10.0 , sp[2*i])
  			straigh_y = [n*yy[2*i] for n in np.ones(len(straigh_x))]
			ax1.plot(straigh_x,straigh_y,'--')
			

		straigh_x = np.linspace(abs(sp[len(yy)-1])/10.0 , sp[len(yy)-1])
  		straigh_y = [n*yy[len(yy)-1] for n in np.ones(len(straigh_x))]
		ax1.plot(straigh_x,straigh_y,'--')
		# print sp,yy

		ax1.set_ylabel('Z(k)')
		ax1.set_ylim(y_list[0],y_list[-1])
		ax1.set_xlabel(x_str1 + r'$\   *1e$' + str(dots),size = 18)

		plt.plot(sp,yy,'black')

		ax1.yaxis.set_ticks_position('left')
		ax1.spines['left'].set_position(('data', 0))
		# ax1.xaxis.set_ticks_position('bottom')
		# ax1.spines['bottom'].set_position(('data', 0))

		if max_ten != None:
			max_ten = max_ten*10**dots
			max_y = np.linspace(y_list[0], y_list[-1],10)
			max_x = [n*max_ten for n in np.ones(len(max_y))]
			plt.annotate('max tensile',xy=(max_ten,0),xytext=(max_ten,0))
					# arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
			ax1.plot(max_x,max_y,'red')

		if max_com != None:
			max_com = max_com*10**dots
			max_y = np.linspace(y_list[0], y_list[-1],10)
			max_x = [n*max_com for n in np.ones(len(max_y))]
			plt.annotate('max compressive',xy=(max_com,0),xytext=(max_com,0))
			ax1.plot(max_x,max_y,'red')
			
		fig.suptitle('strain distribution in lamina')
		plt.grid()
		plt.show()

#-------------------------------------------------------------------------------
def Report_puck(Load,Laminate,layer_num = None ,save = ''):

	Load.apple_to(Laminate)
	P = Puck_Crterion()
	P.Fibre_Failure(Load,layer_num = None)
	FF = P.ret_list

	P.IFF_Modus_A(Load,layer_num = None)
	AA = P.ret_list

	P.IFF_Modus_B(Load,layer_num = None)
	BB = P.ret_list

	P.IFF_Modus_C(Load,layer_num = None)
	CC = P.ret_list

	layer = []
	Model = OrderedDict()

	for i in range(len(FF)):
		F_model = [FF[i],AA[i],BB[i],CC[i]]
		max_F = max(F_model)
		MM = F_model.index(max_F)

		if MM == 0:
			s1 = 'FF'
		if MM == 1:
			s1 = 'IFF model-A'
		if MM == 2:
			s1 = 'IFF model-B'
		if MM == 3:
			s1 = 'IFF model-C'
		if max_F > 1:
			s1  = s1 + '(laminate failure)'

		s = 'Layer_' + str(i) + '_centroid'
		layer.append(s)
		Model[layer[i]] = [max_F,s1]

 	frame = pd.DataFrame(Model)
	frame.index = ['Puck-Value','Failure-Type']

	frame = frame.T
	if save:
		import string
		save = str(save).split('.')[0]
		frame.to_excel(save + '.xlsx')

	return frame

if __name__ == "__main__":
	a = Lamina(5.4e4,1.8e4,8.8e3,v21 = 0.25,Xt = 1.05e3,Xc = 1.04e3,\
											Yt = 28,Yc = 140, S = 42,\
											angle = 0,thickness=5)

	b = Lamina(5.4e4,1.8e4,8.8e3,v21 = 0.25,Xt = 1.05e3,Xc = 1.04e3,\
											Yt = 28,Yc = 140, S = 42,\
											angle = 90,thickness=10)

	LA = Laminate()
	LA.add_Lamina(b)
	LA.add_Lamina(b)
	LA.add_Lamina(a)
	
	LA.update()

	Load = Loading(0,0,0,0,1000,0)
	Load.apple_to(LA)

	print Report_stress(Load,mode = '12')
	print Report_strain(Load,mode = '12')
	# criterian = Failture_Criterion()
	# criterian.Tsai_Hill(Load,layer_num = 1)
	# ret =  criterian.ret_list
	# print ret

	# criterian.Tsai_Hill(Load )
	# ret =  criterian.ret_list
	# print '----Tsai_Hill-->',ret

	# criterian.Hoffman(Load )
	# ret =  criterian.ret_list
	# print '----Hoffman-->',ret
	# print Report_stress(Load,layer_num = 11,mode = '12')
	plot_stress(Load,max_ten = 1.0,mode = 'xy',mode2 = '1')
	# print Report_strain(Load,mode = '12')
	# plot_strain(Load,mode = 'xy',max_ten = None,mode2 = '1')