import re
import numpy as np

def get_jobname()
    mylist = [item for item in os.listdir(os.getcwd()+'/InpFiles/') if item.endswith(".inp")] 
    myints = [int(re.findall(r'\b\d+\b',item)[0]) for item in mylist]
    if not myints:
        myints.append(0)
    jobname = "Job-"+str(max(myints)+1)
    return jobname
    
def compute_separation(xs,ys,rs):
    m = int(len(xs))
    num_pairs = int(m*(m-1)/2)

    pairwise_distances = np.zeros(num_pairs)
    separation = np.zeros(num_pairs)

    idx = 0
    for i in range(0,m):
        for j in range(i,m):
            if i == j:
                continue
                # pairwise_distances[idx] = np.inf
                # gap_size[idx] = tol+rs[i]+rs[j]-pairwise_distances[idx]
                # idx += 1
            else:
                pairwise_distances[idx] = np.sqrt( (xs[j]-xs[i])**2 + (ys[j]-ys[i])**2 )
                separation[idx] = pairwise_distances[idx]-rs[i]-rs[j]
                idx += 1
    return separation