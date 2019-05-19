import numpy as np
import os
import subprocess
from optimization_functions import *

## List of files
# main.py -> main script where we do optimization 
# optimization functions -> helper functions for optimization
# abaqus_evaluations -> script that gets called to run an abaqs model / job etc
# abaqus_functions -> helper functions for abaqus

#Todo:
#Run abaqus from within python script rather than claling this from the command line
#Can do this by writing the variables to a storage file, then executing command line script which reads from known file
#Define file in config

#As anthony said, want to optimize over just the rivet x, y, r
def abaqus_evaluation_wrapper(vec):

    #Function that will take in the arbitrary vector, write to a csv, run abaqus through a separate command, return value.
    total_length = len(vec)
    n = int(total_length/3)

    xs = vec[0*n:1*n]
    ys = vec[1*n:2*n]
    rs = vec[2*n:3*n]

    #Write xs, ys, rs to binaries
    np.save("xs",xs)
    np.save("ys",ys)
    np.save("rs",rs)

    #Generate inp file
    subprocess.run("abaqus cae nogui=abaqus_generate_inp.py", shell=True)

    #Inp file exists, have job name. Move into job files folder, run inp file, move out
    jobname = str(np.load("jobname.npy").astype(str))
    os.chdir("JobFiles")
    print(jobname)
    subprocess.run("abaqus job="+jobname, shell=True)
    os.chdir("..")

    #Extract from odb file next
    
    return True

#Function to generate an initial simplex for a given number of rivets
def generate_xyr_simplex(num_rivets):
    xmin = 0
    xmax = 220
    ymin = 0
    ymax = 100
    rmin = 0
    rmax = 15

    ndim = num_rivets*3
    S = np.random.random_sample((ndim+1,ndim))
    S[:,0*num_rivets:1*num_rivets] = S[:,0*num_rivets:1*num_rivets]*(xmax-xmin) + xmin
    S[:,1*num_rivets:2*num_rivets] = S[:,1*num_rivets:2*num_rivets]*(ymax-ymin) + ymin
    S[:,2*num_rivets:3*num_rivets] = S[:,2*num_rivets:3*num_rivets]*(rmax-rmin) + rmin

    return S

# best = optimize(abaqus_evaluation_deflection_vec, None, 3, 10)
#Run job for generating cae

S = generate_xyr_simplex(1)
abaqus_evaluation_wrapper(S[1])
