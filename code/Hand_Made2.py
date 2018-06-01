
from laminate_analysis_1 import *
from Lamina import Lamina
from Laminate import Laminate
from laminate_Tools import *

if __name__ == "__main__":
	thick = 0.225e-3
	fv = 0.6
	f = Fibre(23e10 ,15e9 , 24e9 ,vf12 = 0.279 ,density = 0 , Xt = 49e8 ,Xc = 441e7 ,\
				Yt = 0  ,Yc = 0 , S = 49e8 )
	
	m = Matrix(Em = 27e8 , Gm= 1.15e9 , vm = 0.3  ,density = 0  ,Xt = 61e6,Xc = 92e6 ,\
				Yt = 0 ,Yc = 0 , S = 45e6 )

	a0 = Lamina(angle = 0 ,thickness= thick )
	a0.Fibre_Matrix_Lamina(fibre = f , matrix = m , fibre_volume = fv)
	a0.Chamis_Model()


	LA = Laminate(degradation = 1e-8)
	LA.add_Lamina(a0)
	LA.add_Lamina(a0)

	LA.add_Lamina(a0)
	LA.add_Lamina(a0)

	LA.add_Lamina(a0)
	LA.add_Lamina(a0)
	LA.add_Lamina(a0)
	LA.add_Lamina(a0)

	LA.add_Lamina(a0)
	LA.add_Lamina(a0)

	LA.add_Lamina(a0)
	LA.add_Lamina(a0)

	LA.update()
	print(LA.Ex ,LA.Ey )

	laminate_step_failure(LA ,  F = [0 ,1 ,0  ,0 ,0, 0] ,layer_num = 5, ply = 1 ,\
		Max_Load = 1e10  , display = 0)

	LA.update()
	print(LA.Ex ,LA.Ey )

 

	# Force = Loading(1,0,0)
	# Force.apple_to(LA)
		
	# print( '\n\n',Force.laminate_stresses_12)

	# Criterion = Failture_Criterion()
	# Criterion.Tsai_Hill(Force,layer_num = None)
	# print( Criterion.ret_list)
