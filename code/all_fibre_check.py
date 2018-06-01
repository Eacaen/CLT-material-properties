
from laminate_analysis_1 import *
from Lamina import Lamina
from Laminate import Laminate
from laminate_Tools import *

if __name__ == "__main__":
	thick = 0.225e-3
	fv = 1
	f = Fibre(23e10 ,15e9 , 24e9 ,vf12 = 0.279 ,density = 0 , Xt = 49e8 ,Xc = 441e7 ,\
				Yt = 23e10  ,Yc = 15e9 , S = 49e8 )


	a0 = Lamina(angle = 0 ,thickness= thick )
	a0.Fibre_Matrix_Lamina(fibre = f , matrix = None , fibre_volume = fv)

	LA = Laminate(degradation = 1e-9)
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

	laminate_step_failure(LA ,  F = [0 ,10 ,0  ,0 ,0, 0] ,layer_num = 0, ply = 0 ,\
		Max_Load = 1e10  , display = 1)

	LA.update()
	print(LA.Ex ,LA.Ey )

	print( a0.E1 , a0.E2 , a0.G12 , a0.v12 , a0.v21 )
	print( a0.Xt , a0.Xc , a0.Yt , a0.Yc , a0.S )

	# Force = Loading(1,0,0)
	# Force.apple_to(LA)
		
	# print( '\n\n',Force.laminate_stresses_12)

	# Criterion = Failture_Criterion()
	# Criterion.Tsai_Hill(Force,layer_num = None)
	# print( Criterion.ret_list)
