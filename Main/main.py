#PYTHON 3
import numpy as np
import os
import subprocess
import re
import time
import csv
from shutil import rmtree
from shutil import copy2
from HelperModule.optimization_functions import * 
from HelperModule.helper_functions import *

def abaqus_evaluation(inpvec,p1):
	#Inputs
	# vec-> input vector. Can be whatever. Interpreted below.
	# p1 -> penalty on constraints
    
    #Constraint values, penalty factors
    Gmin = 20e6         #minimum G -> 20 MPa
    dist_tol = 3        #distance tolerance from frame, other rivets
    min_r = .5			#minimum rivet radius
    
    #Sizing, copy pasted from abaqus script. Can include in input later.
    #Maybe as a config file accessed by both main script and abaqus script.
    cellL = 110.00
    cellW = 110.00
    frameW = 10.00
    t_bat = 3.00

    #Get a job name
    jobname = get_jobname()

    #Process input vector. Clip the positions, rs. Check for separation. Write to input file.
    n = int(len(inpvec)/3)
    xs = inpvec[0*n:1*n]
    ys = inpvec[1*n:2*n]
    rs = inpvec[2*n:3*n]
    rs = np.clip(rs,min_r,min(cellL/4,cellW/4))                  
    xs = np.clip(xs-rs,frameW+rs+dist_tol,cellL-frameW-rs-dist_tol) 
    ys = np.clip(ys-rs,frameW+rs+dist_tol,cellW-frameW-rs-dist_tol)
    inpvec = list(np.concatenate((xs,ys,rs),axis=0))
    inpvec.insert(0,jobname)

    #Check for rivet intersecton
    rivet_separations = compute_separation(xs,ys,rs)
    if any(rivet_separations<=0):
        print(xs,ys,rs)
        print("Skipping because identified rivet intersection!")
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
    output_vec = np.genfromtxt(os.getcwd()+'/OutputFiles/output_vec.csv', delimiter=',')[-1]
    battery_volume = output_vec[1]
    G = output_vec[2]

    #compute penalties. c<=0
    c_G = [Gmin-G]                          
    c_Separation = (dist_tol - rivet_separations)
    c = np.concatenate((c_G,c_Separation), axis=0)

    return -battery_volume + quad_penalty(c,p1)

#Run job for generating cae
if __name__ == "__main__":
    num_rivets = 4
    neval = 200
    nrestarts = 10


    #Remove junk
    rmtree(os.getcwd()+'/OutputFiles/')
    rmtree(os.getcwd()+'/InpFiles/')
    rmtree(os.getcwd()+'/ScratchFiles/')
    os.mkdir(os.getcwd()+'/OutputFiles/')
    os.mkdir(os.getcwd()+'/InpFiles/')
   	os.mkdir(os.getcwd()+'/ScratchFiles/')

    #Prepare and overwrite the input/output csv files by writing zero vectors of appropriate length
    with open(os.getcwd()+'/OutputFiles/output_vec.csv', mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(np.zeros(2))
        writer.writerow(np.zeros(2))

    with open(os.getcwd()+'/InpFiles/input_vec.csv', mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(np.zeros(num_rivets*3))
        writer.writerow(np.zeros(num_rivets*3))

    S = generate_xyr_simplex(num_rivets)
    best_design = abaqus_evaluation_wrapper_local(S[1])
    # print(abaqus_evaluation_wrapper_local(S[1]))


    #Optimize
    # best_design = optimize(abaqus_evaluation_wrapper_local, num_rivets, neval, nrestarts)

    #Save the best design
    with open(os.getcwd()+'/results.csv', mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(best_design)