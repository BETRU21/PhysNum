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
    if f[-5:] == '.json':
        with open(path+f, "r") as j:
            data = json.load(j)

        delta_x = []
        delta_y = []
        time = []
        for k in data.keys():
            time.append(int(k)*2)
            delta_x.append(data[k][0])
            delta_y.append(data[k][1])

        plt.plot(time, delta_x, label=f'$\\Delta_x$ {f[:-5]}', linestyle=ls[i])
        plt.plot(time, delta_y, label=f'$\\Delta_y$ {f[:-5]}', linestyle=ls[i])
        plt.xlabel('Temps [jour]')
        plt.ylabel('Delta [km]')
        plt.legend()
        i += 1

plt.show()
        