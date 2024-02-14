from scipy.integrate import romberg
from Romberg_mod import romberg_mod
from scipy.special import gamma
from uncertainties import ufloat 
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

def nested_simpson(f: callable, a: float, b: float, N: int):
	if N < 3:
		return 'La valeur minimale est 3, car la méthode de simpson nécessite 3 points par approximation'
	N0 = N
	h0 = (b-a)/N
	even = np.linspace(2, N-2, int((N-2)/2), dtype=int)
	odd = np.linspace(1, N-1, int((N-1)/2), dtype=int)
	S0 = (f(a)+f(b)+2*np.sum(list(map(f, a+even*h0))))/3
	T0 = 2/3*np.sum(list(map(f, a+odd*h0)))
	res0 = h0*(S0+2*T0)
	err = np.inf
	lres = [res0]
	lerr = [err]
	while err > 1e-16:
		
		N = N*2
		hi = (b-a)/N
		Si = S0 + T0
		Ti = 2/3*np.sum(list(map(f, a+odd*hi)))
		res = hi*(Si+2*Ti)
		err = (abs((res-res0))/3)/res
		if err > lerr[-1]:
			tes = nested_simpson(f, a, b, N0+1)
			if tes:
				return tes

		lres.append(res)
		lerr.append(err)
		S0 = Si
		T0 = Ti
		res0 = res
	return lres, lerr, N0, a, b


def pi_lambda(Lambda: float, alpha: int, beta: float):
	return 1/gamma(alpha)*Lambda**(alpha-1)*np.exp(-beta*Lambda)*beta**(alpha)

def poisson(x, Lambda):
	return Lambda*np.exp(-Lambda*x)

def product(Lambda, data):
	x = np.sort(np.ediff1d(data))
	return pi_lambda(Lambda, 2, 0.25)*np.prod(poisson(x, Lambda))

def post(Lambda, data):
	return Lambda*product(Lambda, data)


def show_rom(test):
	
	interval = test[1]
	resmat = test[2]
	err = test[4]
	print('Méthode de Romberg:\n')
	print('De lambda = ', interval)
	print('')
	print('%6s %9s ' % ('N', 'h'))
	for i in range(1,len(resmat)-1):
		print('%6d %9f' % (2**i, (interval[1]-interval[0])/(2.**i)), end=' ')
		
		print('Résultat = %.16E' % (resmat[i][-1]), end=' ')
		print('Erreur = %.16E' % err[i], end=' ')
		print('Erreur relative = %.16E' % (err[i]/resmat[i][-1]), end=' ')
		print('')
	print('')
	print('Le résultat final est', '%.16E' % (resmat[i][-1]), end=' ')
	print('après', 2**(len(resmat)-1)+1, 'évaluations de la fonction.')


def show_simp(res):
	interval = [res[-2], res[-1]]
	r = res[0]
	err = res[1]
	print('Méthode de Simpson:\n')
	print('De lambda = ', interval)
	print('')
	print('%6s %9s ' % ('N', 'h'))
	i = 1
	for i in range(1, len(r)):
		print('%6d %9f' % (res[2]*i, (interval[1]-interval[0])/(res[2]*i)), end=' ')
		print('Résultat = %.16E' % (r[i]), end=' ')
		print('Erreur relative = %.16E' % (err[i]), end=' ')
		print('')
	print('')
	print('Le résultat final est', '%.16E' % (r[-1]), end=' ')
	print('avec N = ', res[2]*i,'.')

if __name__ == "__main__":
	path = os.path.abspath("")
	files_name = listNameOfFiles(path)
	
	for nb, name in enumerate(files_name):
		if nb >= 1:
			break

		data_time = readTXT(path+"/"+name)

		product_partial = functools.partial(product, data=data_time)
		post_partial = functools.partial(post, data=data_time)

		re = simpson(product_partial,0,200,int(531))	
		fx = ufloat(re , 1e-16*re)

		results_simpson = nested_simpson(product_partial,0,200,int(3))	
		fx_simpson = ufloat(results_simpson[0][-1], 1e-16*results_simpson[0][-1])

		results_romberg = romberg_mod(product_partial,0,200, show=True, tol=1e-16, rtol=1e-16, divmax=20)
		fx_romberg = ufloat(results_romberg[2][-1][-1], 1e-16*results_romberg[2][-1][-1])

		print('Résultat méthode Simpson = {:.1uP}'.format(fx_simpson))
		print('Résultat méthode Romberg = {:.1uP}'.format(fx_romberg))
		
		lct = simpson(post_partial,0,200,int(1e3))
		lc = ufloat(lct, 1e-16*lct)/fx
		

		x = np.sort(np.ediff1d(data_time)) # Pour voir lambda

		lamb = 1/np.mean(x)

		fig1 = plt.figure()
		plt.hist(x, bins=30)
		plt.show()
		print(f'Lambda_{nb} = {lamb}') #Lambda
		print('Lambda chapeau_{:} = {:.1uP} \n'.format(nb,lc)) # lambda """

		fig2 = plt.figure()
		plt.plot(x, poisson(x,lamb), 'k', label='$\lambda$') 
		plt.plot(x, poisson(x,lc.nominal_value),'r', label='$\hat{\lambda}$')
		plt.yscale('log')
		plt.legend()
		plt.show()
		# Pour graph

		L = np.linspace(0,200,200)
		res = []
		for i in L:
			res.append((product_partial(i)))
		res = np.array(res)

		print(f'Aire sous la courbe des distributions obtenues: {np.sum(res/fx.nominal_value)}')
		fig3 = plt.figure()
		plt.plot(L, res/fx.nominal_value, 'k')
		
		plt.show()

