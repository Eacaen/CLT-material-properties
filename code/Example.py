# coding:utf-8
from Fibre_Matrix import Fibre , Matrix
from Lamina import Lamina
from Laminate import Laminate
from Load import Loading
from Failure_Criterion import Failure_Criterion , Puck_Crterion
from laminate_Tools import *


if __name__ == "__main__":
	a = Lamina(5.4e10 ,1.8e10 , 8.8e9 ,v21 = 0.25  ,Xt = 1.05e9 ,Xc = 1.05e9,\
				Yt = 28e6 ,Yc = 14e6, S = 42e6,\
				angle = 0,thickness=1)

	b = Lamina(5.4e10 ,1.8e10 , 8.8e9 ,v21 = 0.25  ,Xt = 1.05e9 ,Xc = 1.05e9,\
				Yt = 28e6 ,Yc = 14e6, S = 42e6,\
				angle = 90,thickness=10)

	# a = Lamina(5.4e10 ,1.8e10 , 8.8e9 ,v21 = 0.25  ,Xt = 1.05e9 ,Xc = 1.05e9,\
	# 			Yt = 28e6 ,Yc = 14e6, S = 42e6,\
	# 			angle = 45,thickness=1)

	# b = Lamina(5.4e10 ,1.8e10 , 8.8e9 ,v21 = 0.25  ,Xt = 1.05e9 ,Xc = 1.05e9,\
	# 			Yt = 28e6 ,Yc = 14e6, S = 42e6,\
	# 			angle = -45,thickness=1)

	LA = Laminate(degradation = 1e-11)
	LA.add_Lamina(a)
	LA.add_Lamina(b)
	LA.add_Lamina(a)

	# laminate_step_failure(LA ,layer_num = 0 , ply = 0 , display = 0 , show = 1,Fc='Hoffman')
	laminate_step_failure(LA ,layer_num = 0 , ply = 0 , display = 0 , show = 1,Fc='Tsai_Hill')

 

