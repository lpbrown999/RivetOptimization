#PYTHON 3
import numpy as np
import os
import subprocess
import re
import time
import csv
import configparser
from shutil import rmtree
from shutil import copy2
from HelperModule.optimization_functions import * 
from HelperModule.helper_functions import *

def abaqus_evaluation(inpvec,p1):
	#Inputs
	# vec-> input vector, interpreted below
	# nmax-> maximum number of rivets
		
	#Load information from the optimization config
	config = configparser.ConfigParser()
	config.read('optimization_config.ini')

	#Constraints
	Gmin     = float(config['Constraints']['Gmin'])
	dist_tol = float(config['Constraints']['dist_tol'])	
	min_r    = float(config['Constraints']['min_rivet_radius'])
	
	#Cell sizing for clipping the input vector
	cellL  = float(config['CellGeometry']['cellL'])
	cellW  = float(config['CellGeometry']['cellW'])
	frameW = float(config['CellGeometry']['frameW'])
	t_bat  = float(config['CellGeometry']['t_bat'])

	#Optimization stuff
	nmin = int(float(config['Optimization']['min_num_rivets']))
	nmax = int(float(config['Optimization']['max_num_rivets']))

	#Get a job name
	jobname = get_jobname()

	#Process input vector. Reduce to proper number of rivets, clip the positions, rs. 
	#Check for separation. Write to input file.
	n_rivets = int(min(max(inpvec[0],1),nmax))
	xs = inpvec[1::3]
	ys = inpvec[2::3]
	rs = inpvec[3::3]

	xs = xs[0:n_rivets]
	ys = ys[0:n_rivets]
	rs = rs[0:n_rivets]

	rs = np.clip(rs,min_r,min(cellL/4,cellW/4))                  
	xs = np.clip(xs,frameW+rs+dist_tol,cellL-frameW-rs-dist_tol) 
	ys = np.clip(ys,frameW+rs+dist_tol,cellW-frameW-rs-dist_tol)

	#Re-assemble after modification
	inpvec = [jobname,n_rivets]
	for (x,y,r) in zip(xs,ys,rs):
		inpvec.append(x)
		inpvec.append(y)
		inpvec.append(r)

	#Check for rivet intersecton on only the 
	rivet_separations = compute_separation(xs,ys,rs)
	if any(rivet_separations<=0):
		# print(xs,ys,rs)
		print("Skipping because identified rivet intersection.")
		return np.inf

	#Save input vector to be accessed by abaqus
	with open(os.getcwd()+'/InpFiles/input_vec.csv', mode='a+') as f:
		writer = csv.writer(f)
		writer.writerow(inpvec)

	#Run the job
	subprocess.run('abaqus cae nogui=abaqus_script.py', shell=True)
	copy2(os.getcwd()+'/ScratchFiles/%s.odb' % jobname, os.getcwd()+'/OutputFiles/')
	copy2(os.getcwd()+'/ScratchFiles/%s.inp' % jobname, os.getcwd()+'/InpFiles/')

	#Load output information
	data = read_full_csv(os.getcwd()+'/OutputFiles/output_vec.csv')
	output_vec = data[-1]
	battery_volume = float(output_vec[1])
	G = float(output_vec[2])

	#compute penalties. c<=0
	c_G = [Gmin-G]                          
	c_Separation = (dist_tol - rivet_separations)
	c = np.concatenate((c_G,c_Separation), axis=0)

	return -battery_volume + quad_penalty(c,p1)

if __name__ == "__main__":

	#Load optimization parameters from config file
	config = configparser.ConfigParser()
	config.read('optimization_config.ini')

	max_num_rivets = int(float(config['Optimization']['max_num_rivets']))
	num_evals      = int(float(config['Optimization']['num_evals']))
	num_restarts   = int(float(config['Optimization']['num_restarts']))
	penalty        = float(config['Optimization']['penalty'])
	penalty_growth = float(config['Optimization']['penalty_growth'])

	#Remove previous information, create output and input CSV files.
	if os.path.isdir(os.getcwd()+'/OutputFiles/'):
		rmtree(os.getcwd()+'/OutputFiles/')
	if os.path.isdir(os.getcwd()+'/InpFiles/'):
		rmtree(os.getcwd()+'/InpFiles/')
	if os.path.isdir(os.getcwd()+'/ScratchFiles/'):
		rmtree(os.getcwd()+'/ScratchFiles/')

	os.mkdir(os.getcwd()+'/OutputFiles/')
	os.mkdir(os.getcwd()+'/InpFiles/')
	os.mkdir(os.getcwd()+'/ScratchFiles/')

	#Prepare and overwrite the input/output csv files by writing zero vectors of appropriate length
	with open(os.getcwd()+'/OutputFiles/output_vec.csv', mode='w') as f:
		writer = csv.writer(f)
		writer.writerow(np.zeros(1))
		writer.writerow(np.zeros(1))

	with open(os.getcwd()+'/InpFiles/input_vec.csv', mode='w') as f:
		writer = csv.writer(f)
		writer.writerow(np.zeros(1))
		writer.writerow(np.zeros(1))

	#Functions for optimizer
	#Remember that function we optimize has signature f(input,p)
	func_to_opt = lambda inpvec, p: abaqus_evaluation(inpvec,p)
	S_gen = lambda: generate_n_x_y_r_simplex()

	# func_to_opt([2,76,55,6.5,34,55,6.5], penalty)


	# Optimize
	best_design = optimize(func_to_opt, S_gen, num_evals, num_restarts, penalty, penalty_growth)
