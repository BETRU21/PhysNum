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
	d_FU = df_u(T, FU)

	ax[0].set_title("Méthode par relaxation")
	ax[0].plot(T, FU_analytique)
	ax[0].plot(T, FU, linestyle="-.")


	# Newton-Raphson
	ax[1].set_title("Méthode par Newton-Raphson")
	ax[1].plot(T, FU_analytique)

	FU = []
	for T in np.linspace(0,1,21):
		u = 0.1
		for i in range(1000):
			if df_u(T,u) == 0:
				break
			u = u - f_u(T, u)/df_u(T,u)
			print(u)
		FU.append(u)

	T = np.linspace(0,1,21)

	print(FU)

	FU = np.array(FU)
	d_FU = df_u(T, FU)


	ax[1].plot(T, FU, linestyle="-.")
	plt.show()