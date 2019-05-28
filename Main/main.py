#PYTHON 3
import numpy as np
import os
import subprocess
import re
import time
import csv
from shutil import copy2
from HelperModule.optimization_functions import * 

def abaqus_evaluation_wrapper_local(vec):
    
    #Constraint values, penalty factors
    Gmin = 0         #minimum G -> 20 MPa
    dist_tol = 3        #distance tolerance from frame, other rivets
    p1 = 100            #penalty weighting

    #Sizing, copy pasted from abaqus script
    #Could include in input vector in the future but not today
    cellL = 110.00
    cellW = 110.00
    frameW = 10.00
    t_bat = 3.00

    #From the input vector, and then clip so rivet locations are valid.
    # 1. rivets cannot be over or under sized
    # 2. cannot be outside of frame.
    n = int(len(vec)/3)
    xs = vec[0*n:1*n]
    ys = vec[1*n:2*n]
    rs = vec[2*n:3*n]

    rs = np.clip(rs,dist_tol,min(cellL/4,cellW/4))                  
    xs = np.clip(xs-rs,frameW+rs+dist_tol,cellL-frameW-rs-dist_tol) 
    ys = np.clip(ys-rs,frameW+rs+dist_tol,cellW-frameW-rs-dist_tol)

    #Check if any rivets are within distance tolerance of each other. If they are, return a high value (penalized)
    #Think about: adding a "ramping constraint" as the pieces get too close together
    rivet_separations = compute_separation(xs,ys,rs)
    if any(rivet_separations<=0):
        print(xs,ys,rs)
        print("Skipping because identified rivet intersection!")
        return np.inf

    #Made it to here means rivets do not intersect
    #Get job name
    mylist = [item for item in os.listdir(os.getcwd()+'/InpFiles/') if item.endswith(".inp")] 
    myints = [int(re.findall(r'\b\d+\b',item)[0]) for item in mylist]
    if not myints:
        myints.append(0)
    jobname = "Job-"+str(max(myints)+1)

    #Save input vector to be accessed by abaqus
    vec = np.concatenate((xs,ys,rs),axis=0)
    with open(os.getcwd()+'/InpFiles/input_vec.csv', mode='a+') as f:
        writer = csv.writer(f)
        writer.writerow(vec)

    #Run the job
    subprocess.run('abaqus cae nogui=abaqus_script.py -- %s' % jobname, shell=True)
    copy2(os.getcwd()+'/ScratchFiles/%s.odb' % jobname, os.getcwd()+'/OutputFiles/')
    copy2(os.getcwd()+'/ScratchFiles/%s.inp' % jobname, os.getcwd()+'/InpFiles/')

    #Load output information
    output_vec = np.genfromtxt(os.getcwd()+'/OutputFiles/output_vec.csv', delimiter=',')[-1]
    battery_volume = output_vec[0]
    G = output_vec[1]
    # print(G)

    #compute penalties. c<=0
    c_G = [Gmin-G]                          #Gmin<=G
    c_Separation = (dist_tol - rivet_separations)*1000
    c = np.concatenate((c_G,c_Separation), axis=0)
    penalty = quad_penalty(c)

    #Now return the objective + the penalty (note we are minimizing)
    return -battery_volume + p1*penalty

#Run job for generating cae
if __name__ == "__main__":
    num_rivets = 4
    neval = 200
    nrestarts = 10

    #Prepare and overwrite the input/output csv files by writing zero vectors of appropriate length
    with open(os.getcwd()+'/OutputFiles/output_vec.csv', mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(np.zeros(2))
        writer.writerow(np.zeros(2))

    with open(os.getcwd()+'/InpFiles/input_vec.csv', mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(np.zeros(num_rivets*3))
        writer.writerow(np.zeros(num_rivets*3))

    # S = generate_xyr_simplex(num_rivets)
    # print(abaqus_evaluation_wrapper_local(S[1]))


    #Optimize
    best_design = optimize(abaqus_evaluation_wrapper_local, num_rivets, neval, nrestarts)

    #Save the best design
    with open(os.getcwd()+'/results.csv', mode='w') as f:
        writer = csv.writer(f)
        writer.writerow(best_design)