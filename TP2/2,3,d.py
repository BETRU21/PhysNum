import matplotlib.pyplot as plt
import numpy as np

def f_u(T, u):
	return (1)/( (1 + 4*T -4*T*u)**2 )-u

def df_u(T,u):
	return (8*T)/(( 1-4*T*(u-1) )**3)-u


fig = plt.figure()
t = 0.1
point_list = []
x0 = 0
point_list.append((x0, f_u(t, x0)))
check_ratio = []
for i in range(20):
    x,y = point_list[-1]

    y = x - f_u(t, x)/df_u(t,x)
    check_ratio.append(f_u(t, x)/df_u(t,x))
    print(y)
    point_list.append((x,y))
    x = y
    point_list.append((x,y))

point_list = np.array(point_list)
X,Y = point_list.T
xy = np.linspace(-4,4,1000)
plt.ylim(-4,6)
plt.xlim(-4,4)
plt.axhline(y=0, color='k', linewidth=0.5)
plt.plot(xy, f_u(t, xy), 'r', label='Fonction étudiée')
plt.plot(xy, df_u(t, xy), 'g', label='Dérivé de la fonction étudiée')
plt.plot(X,f_u(t, X), 'k.', linestyle='--', label= 'Étapes de résolution')
plt.legend()
plt.show()