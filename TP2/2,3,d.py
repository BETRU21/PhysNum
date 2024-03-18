import matplotlib.pyplot as plt
import numpy as np

def f_u2(T, u):
	return (1)/( (1 + 4*T -4*T*u)**2 )-u

def df_u2(T,u):
	return (8*T)/(( 1-4*T*(u-1) )**3)-u


fig = plt.figure()
t = 0.1
point_list = []
x0 = 0.5
point_list.append((x0, f_u2(t, x0)))
for i in range(100):
    x,y = point_list[-1]

    y = x - f_u2(t, x)/df_u2(t,x)
    point_list.append((x,y))
    x = y
    point_list.append((x,y))
print(f'Résultat méthode par Newton-Raphson: {round(y,10)}')
print(f'Résultat théorique u1: {1}')

point_list = np.array(point_list)
X,Y = point_list.T
xy = np.linspace(-4,10,1000)
plt.ylim(-4,6)
plt.xlim(-4,10)
plt.axhline(y=0, color='k', linewidth=0.5)
plt.plot(xy, f_u2(t, xy), 'r', label='Fonction étudiée')
#plt.plot(xy, df_u2(t, xy), 'g', label='Dérivé de la fonction étudiée')
plt.plot(X,f_u2(t, X), 'k.', linestyle='--', label= 'Étapes de résolution')
plt.legend()
plt.show()