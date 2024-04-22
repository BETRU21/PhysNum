import numpy as np
import os
import json
import matplotlib.pyplot as plt

import matplotlib as mpl

# Set the default color cycle
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=["r", "k", "b", 'orange']) 


path = 'projet\\'
files = os.listdir(path)

i = 0
ls = ['-', (0, (5,8))]
fig = plt.figure()

for f in files:
    if f[-4:] == '.txt' and f[:-4] != 'temp':
        
        data = np.loadtxt(path+f, delimiter=',')
        time = np.linspace(2, len(data[:,0])*2, len(data[:,0]))

        plt.plot(time, data[:,0], label=f'$\\Delta_x$ {f[:-5]}', linestyle=ls[i])
        plt.plot(time, data[:,1], label=f'$\\Delta_y$ {f[:-5]}', linestyle=ls[i])
        plt.xlabel('Temps [jour]')
        plt.ylabel('Delta [km]')
        plt.legend()
        i += 1
plt.savefig(path+'test.png', dpi=600)
plt.show()
        