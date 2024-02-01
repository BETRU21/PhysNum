from scipy.integrate import romberg
from scipy.special import gamma
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


def pi_lambda(alpha: int, beta: float):
	lamb = np.linspace(0,200,201)
	return 1/gamma(alpha)*lamb**(alpha-1)*np.exp(-beta*lamb)*beta**(alpha)


if __name__ == "__main__":
	path = os.path.abspath("")
	files_name = listNameOfFiles(path)

	time_0 = readTXT(path+"/"+files_name[0])
	time_1 = readTXT(path+"/"+files_name[1])
	time_2 = readTXT(path+"/"+files_name[2])

	testSimpson = simpson(x2,0,3,10000)
	testRomberg = romberg(x2,0,3) # Il va sûrement falloir faire la notre pour contrôler N (on peut peut-être s'en sortir avec la fonction 'romb' de scipy)
	testpi_lambda = pi_lambda(2, 0.25)

	print(testSimpson)
	print(testRomberg)
	print(testpi_lambda)
