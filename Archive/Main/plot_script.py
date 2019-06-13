import matplotlib.pyplot as plt
import numpy as np
import os
import configparser

from HelperModule.helper_functions import *


#Load the output data
data = read_full_csv(os.getcwd()+'/OutputFiles/output_vec.csv')
data = data[2:]

#Load parameters
config = configparser.ConfigParser()
config.read('optimization_config.ini')

#Constraints
Gmin = float(config['Constraints']['Gmin'])

#Make list of the volumes, gs
battery_volumes = []
Gs = []
for row in data:
	battery_volumes.append(float(row[1]))
	Gs.append(float(row[2]))
battery_volumes = np.array(battery_volumes)
Gs = np.array(Gs)

#Create vector for only improved poitns
battery_volumes_filtered = [0]
Gs_filtered = [0]
for G, battery_volume in zip(Gs,battery_volumes):
	if G>=Gmin and battery_volume>=battery_volumes_filtered[-1]:
		battery_volumes_filtered.append(battery_volume)
		Gs_filtered.append(G)
	else:
		battery_volumes_filtered.append(battery_volumes_filtered[-1])
		Gs_filtered.append(Gs_filtered[-1])

battery_volumes_filtered = np.array(battery_volumes_filtered[1:])
Gs_filtered = np.array(Gs_filtered[1:])

num_evals_to_show = 400
max_battery_volume = 90*90*5


fig1, ax1 = plt.subplots()
ax1.plot(Gmin*np.ones(num_evals_to_show)*1e-6,color='r',label='Minimum G')
ax1.plot(Gs_filtered[0:num_evals_to_show]*1e-6,color='b',label='Best Design')
ax1.plot(Gs[0:num_evals_to_show]*1e-6,color='gray',alpha=.5,label='Current Evaluation')

ax1.legend()
ax1.set(xlabel="Evaluation Number", ylabel="G (MPa)")
plt.savefig(os.getcwd()+"/Figures/gs.png",dpi=300)

fig2, ax2 = plt.subplots()
ax2.plot(battery_volumes_filtered[0:num_evals_to_show]/max_battery_volume,color='b',label='Best Design')
ax2.plot(battery_volumes[0:num_evals_to_show]/max_battery_volume,color='gray',alpha=.5,label='Current Evaluation')
ax2.legend()
ax2.set(xlabel="Evaluation Number", ylabel=r"Percent of Max Battery Volume")
plt.savefig(os.getcwd()+"/Figures/vols.png",dpi=300)
