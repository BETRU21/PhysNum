import matplotlib.pyplot as plt
import numpy as np

def f_u(T, u):
	return (1)/( (1 + 4*T -4*T*u)**2 )

def df_u(T,u):
	return (8*T)/(( 1-4*T*(u-1) )**3)

def u_2(T):
	return 1 - ( 2*T-1 + 2*np.sqrt(T**2+T) )/( 4*T )

def u_1(T):
	return np.ones(T.shape)

def R(T,u):
	return 1 - ( 1-T*(1-u))/( 1+4*T*(1-u) )



if __name__ == "__main__":
	fig, ax = plt.subplots(nrows=1, ncols=2)

	# relaxation 
	FU = []
	for T in np.linspace(0,1,21):
		u = 0.1
		for i in range(1000):
			u = f_u(T, u)
		FU.append(u)

	

	T = np.linspace(0,1,21)

	FU_analytique = []
	for t in T:
		if t > 0.125:
			FU_analytique.append(u_2(t))
		else:
			FU_analytique.append(u_1(t))

	FU = np.array(FU)

	ax[0].set_title("Méthode par relaxation")
	ax[0].plot(T, FU_analytique)
	ax[0].plot(T, FU, linestyle="--", color="r")
	ax[0].set_xlabel("T")
	ax[0].set_ylabel("u_min")


	# Newton-Raphson
	ax[1].set_title("Méthode par Newton-Raphson")
	ax[1].plot(T, FU_analytique)

	FU = []
	for T in np.linspace(0,1,21):
		u = 1.5
		for i in range(100):
			if df_u(T,u) == 0:
				break
			u = u - f_u(T, u)/df_u(T,u)
		FU.append(u)

	T = np.linspace(0,1,21)

	print(FU)

	FU = np.array(FU)
	ax[1].plot(T, FU, linestyle="--", color="r")


	fig = plt.figure()
	T = 0.5
	u = np.linspace(0,5,1000)
	plt.plot(u, f_u(T,u), label='f(u)')
	plt.plot(u, df_u(T,u), label="f'(u)")
	plt.legend()


	fig = plt.figure()
	T = 0.5
	point_list = []
	x0 = 0.1
	point_list.append((x0, 0))
	for i in range(1000):
		x,y = point_list[-1]
		y = f_u(T, x)

		point_list.append((x,y))
		x = y
		point_list.append((x,y))
	print(y)
	point_list = np.array(point_list)
	X,Y = point_list.T
	xy = np.linspace(0,2,100)
	plt.ylim(0,y*1.1)
	plt.xlim(0,x*1.1)
	plt.plot(xy,xy)
	plt.plot(xy, f_u(T, xy))
	plt.plot(X,Y)

	print('newton')
	fig = plt.figure()
	T = 0.1
	point_list = []
	x0 = 3
	point_list.append((x0, 0))
	for i in range(20):
		x,y = point_list[-1]

		y = x - f_u(T, x)/df_u(T,x)
		print(df_u(T,x))
		
		point_list.append((x,y))
		x = y
		point_list.append((x,y))
	print(y)
	point_list = np.array(point_list)
	X,Y = point_list.T
	xy = np.linspace(0,4,100)
	plt.ylim(0,10)
	plt.xlim(0,4)
	plt.plot(xy,xy)
	plt.plot(xy, f_u(T, xy))
	plt.plot(X,Y)


	plt.show()