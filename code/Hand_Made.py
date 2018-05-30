
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

	a45 = Lamina(angle = 45 ,thickness= thick )
	a45.Fibre_Matrix_Lamina(fibre = f , matrix = m , fibre_volume = fv)
	a45.Chamis_Model()

	a_45 = Lamina(angle = -45 ,thickness= thick )
	a_45.Fibre_Matrix_Lamina(fibre = f , matrix = m , fibre_volume = fv)
	a_45.Chamis_Model()

	b30 = Lamina(angle = 30 ,thickness= thick )
	b30.Fibre_Matrix_Lamina(fibre = f , matrix = m , fibre_volume = fv)
	b30.Chamis_Model()

	b_30 = Lamina(angle = -30 ,thickness= thick )
	b_30.Fibre_Matrix_Lamina(fibre = f , matrix = m , fibre_volume = fv)
	b_30.Chamis_Model()

	c15 = Lamina(angle = 15 ,thickness= thick )
	c15.Fibre_Matrix_Lamina(fibre = f , matrix = m , fibre_volume = fv)
	c15.Chamis_Model()

	c_15 = Lamina(angle = -15 ,thickness= thick )
	c_15.Fibre_Matrix_Lamina(fibre = f , matrix = m , fibre_volume = fv)
	c_15.Chamis_Model()

	LA = Laminate(degradation = 1e-5)
	LA.add_Lamina(a45)
	LA.add_Lamina(a_45)

	LA.add_Lamina(b30)
	LA.add_Lamina(b_30)

	LA.add_Lamina(c15)
	LA.add_Lamina(c_15)
	LA.add_Lamina(c_15)
	LA.add_Lamina(c15)

	LA.add_Lamina(b_30)
	LA.add_Lamina(b30)

	LA.add_Lamina(a_45)
	LA.add_Lamina(a45)

	LA.update()
	print(LA.Ex ,LA.Ey )

	laminate_step_failure(LA ,  F = [0 ,1e3 ,0  ,0 ,0, 0] ,layer_num = 5, ply = 1 ,\
		Max_Load = 1e10  , display = 0)

	LA.update()
	print(LA.Ex ,LA.Ey )

	print( a45.E1 , a45.E2 , a45.G12 , a45.v12 , a45.v21 )
	print( a45.Xt , a45.Xc , a45.Yt , a45.Yc , a45.S )
	print( a0.Xt , a0.Xc , a0.Yt , a0.Yc , a0.S )

	# Force = Loading(1,0,0)
	# Force.apple_to(LA)
		
	# print( '\n\n',Force.laminate_stresses_12)

	# Criterion = Failture_Criterion()
	# Criterion.Tsai_Hill(Force,layer_num = None)
	# print( Criterion.ret_list)
