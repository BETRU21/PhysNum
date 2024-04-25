import numpy as np
import os
import matplotlib.pyplot as plt
from cycler import cycler
import seaborn as sns
sns.set_theme(style="ticks", palette="deep")

plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.spines.top"] = False

nb_of_files = 2
# Set the default color cycle
cmap = plt.get_cmap('brg')
colors = cmap(np.linspace(0, 1, 3))
plt.rc('axes', prop_cycle=(cycler('color', colors) +
                           cycler('linestyle', ['-', '--', '-.'])))

path = 'projet\\'
files = os.listdir(path)

i = 0
fig = plt.figure(figsize=(14,8))

for f in files:
    if f[-4:] == '.txt' and f[:-4] != 'temp':
        
        data = np.loadtxt(path+f, delimiter=',')
        time = np.linspace(1, len(data[:,0])*2, len(data[:,0]))

        plt.plot(time, data[:,0], label=f'$\\Delta_x$')
        plt.plot(time, data[:,1], label=f'$\\Delta_y$')
        #try:
        #plt.plot(time,np.sqrt(data[:,0]**2 + data[:,1]**2, data[:,2]**2), label=f'$\\Delta_r$ {f[:-4]}')
            
        #except IndexError as e:
        plt.plot(time,np.sqrt(data[:,0]**2 + data[:,1]**2), label=f'$\\Delta_r$')
            #pass
        plt.xlabel('Temps [jour]')
        plt.ylabel('Delta [km]')
        plt.legend()
        i += 1
plt.savefig(path+'test.png', dpi=600)
plt.show()
        