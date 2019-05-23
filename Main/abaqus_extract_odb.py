import numpy as np
import os
import sys
from HelperModule.abaqus_functions import *

def abaqus_extract_odb(jobname):
    maxu3,minu3 = get_max_min_disp(name=jobname)
    val_array = np.array([maxu3,minu3])
    np.save(jobname+'.npy',val_array)
    return True

if __name__ == "__main__":
    os.chdir("/home/users/lpbrown/SRCC/OutputFiles/")
    jobname = sys.argv[-1]
    abaqus_extract_odb(jobname)
