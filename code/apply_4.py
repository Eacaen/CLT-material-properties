# define lamina directly

from laminate_analysis_1 import *

if __name__ == "__main__":
	a = Lamina(138,9,6.9,v12 = 0.3 , v21=0.0196,Xt = 1.05e3,Xc = 1.05e3,\
				Yt = 2.8e1,Yc = 14e1, S = 1.4e1,\
				angle = 45,thickness=0.25)


	b = Lamina(138,9,6.9,v12 = 0.3 , v21=0.0196,Xt = 1.05e3,Xc = 1.05e3,\
				Yt = 2.8e1,Yc = 14e1, S = 1.4e1,\
				angle = -45,thickness=0.25)

	print 'a.matrix_Q',a.matrix_Q
	print 'a.matrix_Q_bar',a.matrix_Q_bar
	print 'b.matrix_Q',b.matrix_Q
	print 'b.matrix_Q_bar',b.matrix_Q_bar

	LA = Laminate()
	LA.add_Lamina(a)
	LA.add_Lamina(b)
	LA.add_Lamina(b)
	LA.add_Lamina(a)
	LA.update()
	print('A',LA.A)
	print('B',LA.B)
	print('D',LA.D)
