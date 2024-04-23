import numpy as np
import os
import matplotlib.pyplot as plt
from cycler import cycler

import matplotlib as mpl

# Set the default color cycle
cmap = plt.get_cmap('jet')
colors = cmap(np.linspace(0, 1, 12))
linestyle_cycler = cycler('linestyle',['-','--',':','-.'])

plt.rc('axes', prop_cycle=(cycler('color', colors) +
                           cycler('linestyle', ['-', '--', ':', '-.']*3)))

path = 'projet\\'
files = os.listdir(path)

i = 0
fig = plt.figure(figsize=(14,8))

for f in files:
    if f[-4:] == '.txt' and f[:-4] != 'temp':
        
        data = np.loadtxt(path+f, delimiter=',')
        time = np.linspace(2, len(data[:,0])*2, len(data[:,0]))

        plt.plot(time, data[:,0], label=f'$\\Delta_x$ {f[:-5]}' )
        plt.plot(time, data[:,1], label=f'$\\Delta_y$ {f[:-5]}')
        try:
            plt.plot(time, data[:,2], label=f'$\\Delta_z$ {f[:-5]}')
        except IndexError as e:
            pass
        plt.xlabel('Temps [jour]')
        plt.ylabel('Delta [km]')
        plt.legend()
        i += 1
plt.savefig(path+'test.png', dpi=600)
plt.show()
        