
from laminate_analysis_1 import *
from Lamina import Lamina
from Laminate import Laminate
from laminate_Tools import *

if __name__ == "__main__":
	thick = 0.125e-3
	fv = 0.6
	f = Fibre(23e10 ,15e9 , 24e9 ,vf12 = 0.279 ,density = 0 , Xt = 49e8 ,Xc = 441e7 ,\
				Yt = None  ,Yc = None , S = 49e8 )
	
	m = Matrix(Em = 27e8 , Gm= 1e9 , vm = 0.363  ,density = 0  ,Xt = 61e6,Xc = 92e6 ,\
				Yt = None ,Yc = None , S = 45e6 )

	a0 = Lamina(angle = 0 ,thickness= thick )
	a0.Fibre_Matrix_Lamina(fibre = f , matrix = m , fibre_volume = fv)


	print( a0.E1 , a0.E2 , a0.G12 , a0.v12 , a0.v21 )

	print( a0.Xt , a0.Xc , a0.Yt , a0.Yc , a0.S )

	
	print("used chamis model ------- >> ")
	a0.Fibre_Matrix_Lamina(fibre = f , matrix = m , fibre_volume = fv)
	a0.Chamis_Model()
	print( a0.E1 , a0.E2 , a0.G12 , a0.v12 , a0.v21 )
	print( a0.Xt , a0.Xc , a0.Yt , a0.Yc , a0.S )