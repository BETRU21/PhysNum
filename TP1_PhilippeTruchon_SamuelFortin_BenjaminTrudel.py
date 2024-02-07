from scipy.integrate import romberg
from Romberg_mod import romberg_mod
from scipy.special import gamma
import matplotlib.pyplot as plt
import numpy as np
import functools
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

def pi_lambda(Lambda: float, alpha: int, beta: float):
	return 1/gamma(alpha)*Lambda**(alpha-1)*np.exp(-beta*Lambda)*beta**(alpha)

def poisson(x, Lambda):
	return Lambda*np.exp(-Lambda*x)

def product(Lambda, data):
	x = np.sort(np.ediff1d(data))
	return pi_lambda(Lambda, 2, 0.25)*np.prod(poisson(x, Lambda))

def post(Lambda, data):
	return Lambda*product(Lambda, data)

if __name__ == "__main__":
	path = os.path.abspath("")
	files_name = listNameOfFiles(path)

	for nb, name in enumerate(files_name):
		data_time = readTXT(path+"/"+name)

		product_partial = functools.partial(product, data=data_time)
		post_partial = functools.partial(post, data=data_time)

		y = simpson(product_partial,0,200,int(1e3))	
		#yr = romberg(product_partial,0,200, show=True, tol=1e-32)
		test = romberg_mod(product_partial,0,200, show=True, tol=1e-16, divmax=20)
		print(test[3])
		#print(yr)
		print(f'f(x)_{nb} = {y}')
		lc = simpson(post_partial,0,200,int(1e3))/y

		x = np.sort(np.ediff1d(data_time)) # Pour voir lambda
		print(f'Lambda_{nb} {1/np.mean(x)}') #Lambda
		print(f'Lambda chapeau {nb} = {lc} \n') # lambda chapeau

