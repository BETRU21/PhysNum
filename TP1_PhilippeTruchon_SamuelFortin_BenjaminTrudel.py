from scipy.integrate import romberg
from scipy.special import gamma
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
import fnmatch
import os

def listNameOfFiles(directory: str, extension="txt"):
	found_files = []
	for file in os.listdir(directory):
		if fnmatch.fnmatch(file, f'*.{extension}'):
			found_files.append(file)
	return found_files

def readTXT(path: str):
	fich = open(path, "r")
	fich_str = list(fich)
	fich.close()
	x = []
	for i in fich_str:
		elem_str = i.replace("\n", "")
		x.append(float(elem_str))
	return np.array(x)

def simpson(f: callable, a: float, b: float, N: int):
	h = (b-a)/N
	s1 = 0.0
	for i in range(1,N,2):
		s1 += f(a+i*h)
	s2 = 0.0
	for i in range(2,N,2):
		s2 += f(a+i*h)
	return (f(a)+f(b)+4.0*s1+2.0*s2)*h/3.0

def x2(x):
	return x**2

def pi_lambda(Lambda: float, alpha: int, beta: float):
	return 1/gamma(alpha)*Lambda**(alpha-1)*np.exp(-beta*Lambda)*beta**(alpha)

def poisson(x, Lambda):
	return Lambda*np.exp(-Lambda*x)

def product0(Lambda):
	path = os.path.abspath("")
	files_name = listNameOfFiles(path)
	time_0 = readTXT(path+"/"+files_name[0])
	x = np.sort(np.ediff1d(time_0))
	return pi_lambda(Lambda, 2, 0.25)*np.prod(poisson(x, Lambda))

def post0(Lambda):
	return Lambda*product0(Lambda)

def product1(Lambda):
	path = os.path.abspath("")
	files_name = listNameOfFiles(path)
	time_1 = readTXT(path+"/"+files_name[1])
	x = np.sort(np.ediff1d(time_1))
	return pi_lambda(Lambda, 2, 0.25)*np.prod(poisson(x, Lambda))

def post1(Lambda):
	return Lambda*product1(Lambda)

def product2(Lambda):
	path = os.path.abspath("")
	files_name = listNameOfFiles(path)
	time_2 = readTXT(path+"/"+files_name[2])
	x = np.sort(np.ediff1d(time_2))
	return pi_lambda(Lambda, 2, 0.25)*np.prod(poisson(x, Lambda))

def post2(Lambda):
	return Lambda*product2(Lambda)

def Compute_time_0(show_plot=True):
	L = np.linspace(0,200,200)
	res = []
	for i in L:
		res.append((product0(i)))

	y = simpson(product0,0,200,int(1e3))	
	print(f'f(x)_0 = {y}')
	lc = simpson(post0,0,200,int(1e3))/y
	

	x = np.sort(np.ediff1d(time_0)) # Pour voir lambda
	print(f'Lambda_0 {1/np.mean(x)}') #Lambda

	print(f'Lambda chapeau 0 = {lc}') # lambda chapeau
	print("")

	if show_plot:
		plt.plot(L, res/y, 'k')
		plt.show()

def Compute_time_1(show_plot=True):
	L = np.linspace(0,200,200)
	res = []
	for i in L:
		res.append((product1(i)))

	y = simpson(product1,0,200,int(1e3))	
	print(f'f(x)_1 = {y}')
	lc = simpson(post1,0,200,int(1e3))/y
	

	x = np.sort(np.ediff1d(time_1)) # Pour voir lambda
	print(f'Lambda_1 {1/np.mean(x)}') #Lambda

	print(f'Lambda chapeau 1 = {lc}') # lambda chapeau
	print("")

	if show_plot:
		plt.plot(L, res/y, 'k')
		plt.show()

def Compute_time_2(show_plot=True):
	L = np.linspace(0,200,200)
	res = []
	for i in L:
		res.append((product2(i)))

	y = simpson(product2,0,200,int(1e3))	
	print(f'f(x)_2 = {y}')
	lc = simpson(post2,0,200,int(1e3))/y
	

	x = np.sort(np.ediff1d(time_2)) # Pour voir lambda
	print(f'Lambda_2 {1/np.mean(x)}') #Lambda

	print(f'Lambda chapeau 2 = {lc}') # lambda chapeau
	print("")

	if show_plot:
		plt.plot(L, res/y, 'k')
		plt.show()

if __name__ == "__main__":
	path = os.path.abspath("")
	files_name = listNameOfFiles(path)

	time_0 = readTXT(path+"/"+files_name[0])
	time_1 = readTXT(path+"/"+files_name[1])
	time_2 = readTXT(path+"/"+files_name[2])

	testSimpson = simpson(x2,0,3,10000)
	testRomberg = romberg(x2,0,3) # Il va sûrement falloir faire la notre pour contrôler N (on peut peut-être s'en sortir avec la fonction 'romb' de scipy)
	
	Compute_time_0(False)
	Compute_time_1(False)
	Compute_time_2(False)



	


	


