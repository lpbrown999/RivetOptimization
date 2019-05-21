#PYTHON 3
#This gets called by main.sh
import numpy as np
import os
import re
import time
from HelperModule import bash_functions

# from HelperModule.optimization_functions import *
# from HelperModule.bash_functions import *

def abaqus_evaluation_wrapper(vec):

    #Function that will take in the arbitrary vector, write to a csv, run abaqus through a separate command, return value.
    total_length = len(vec)
    n = int(total_length/3)

    xs = vec[0*n:1*n]
    ys = vec[1*n:2*n]
    rs = vec[2*n:3*n]

    #Write xs, ys, rs to binaries for input generating script to load.
    np.save(os.getcwd()+'/ScratchFiles/xs.npy',xs)
    np.save(os.getcwd()+'/ScratchFiles/ys.npy',ys)
    np.save(os.getcwd()+'/ScratchFiles/rs.npy',rs)

    #Get job name
    mylist = [item for item in os.listdir(os.getcwd()+'/InpFiles/') if item.endswith(".inp")] 
    myints = [int(re.findall(r'\b\d+\b',item)[0]) for item in mylist]
    if not myints:
        myints.append(0)
    jobname = "Job-"+str(max(myints)+1)

    #Write bash script to generate the inp file, then run it.
    bash_functions.write_generate_inp_script(jobname,"abaqus_generate_inp.sh")
    os.system("sbatch abaqus_generate_inp.sh")

    while not os.path.isfile(os.getcwd()+'/InpFiles/'+jobname+'.inp'):
        time.sleep(2)
        print('Waiting for %s.inp to generate.' % jobname)

    print('%s.inp generated. Submitting for analysis.' % jobname)

    #Write bash script to run the job, then run it.
    bash_functions.write_job_submission_script(jobname,"abaqus_job_submission.sh")
    os.system("sbatch abaqus_job_submission.sh")

    while not os.path.isfile(os.getcwd()+'/OutputFiles/'+jobname+'.odb'):
        time.sleep(2)
        print('Waiting for %s to finish analysis.' % jobname)
    print('%s finished analyzing. Inspecting ODB.' % jobname)
    

    #Extract results from odb file. Since this requires a cae session, 
    #once again write a bash script to schedule a job
    bash_functions.write_odb_extraction_script(jobname,"abaqus_odb_extraction.sh")
    os.system("sbatch abaqus_odb_extraction.sh")

    while not os.path.isfile(os.getcwd()+'/OutputFiles/'+jobname+'.npy'):
        time.sleep(2)
        print('Waiting for %s.odb to finish extraction.' % jobname)
        
    print('%s.odb finished extraction. Returning values!' % jobname)

    output_values = np.load(os.getcwd()+"/OutputFiles/"+jobname+".npy")
    maxu3 = output_values[0]
    minu3 = output_values[1]

    #Clean up the results?
    # os.system("rm *.log")
    # os.system("rm *.output")
    # os.system("rm *.rpy*")
    
    return minu3

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

#best = optimize(abaqus_evaluation_deflection_vec, None, 3, 10)

#Run job for generating cae
if __name__ == "__main__":
    S = generate_xyr_simplex(2)
    minu3_1 =  abaqus_evaluation_wrapper(S[1])
    minu3_2 =  abaqus_evaluation_wrapper(S[2])
    print("%f minu3!" % minu3_1)
    print("%f minu3!" % minu3_2)