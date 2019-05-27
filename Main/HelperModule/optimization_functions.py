import numpy as np
import math
def generate_xyr_simplex(num_rivets):
    xmin = 0
    xmax = 110
    ymin = 0
    ymax = 110
    rmin = 0
    rmax = 10

    ndim = num_rivets*3
    S = np.random.random_sample((ndim+1,ndim))
    S[:,0*num_rivets:1*num_rivets] = S[:,0*num_rivets:1*num_rivets]*(xmax-xmin) + xmin
    S[:,1*num_rivets:2*num_rivets] = S[:,1*num_rivets:2*num_rivets]*(ymax-ymin) + ymin
    S[:,2*num_rivets:3*num_rivets] = S[:,2*num_rivets:3*num_rivets]*(rmax-rmin) + rmin

    return S

#Unconstrained optimization method nelder mead-simplex!
def nelder_mead(f, S, n, alpha=1.0, beta=2.0, gamma=0.5):
    #f -> function 
    #S -> Initial simplex. ndim+1 points by ndim dimensions.
    #n -> allowed evaluations
    nevals, y_arr = len(S), np.array(list(map(f,S)))

    while nevals < n:
        p = np.argsort(y_arr)           #Sorted indexes based on funciton values
        S, y_arr = S[p], y_arr[p]
        xl, yl = S[0], y_arr[0]         #location, lowest value
        xh, yh = S[-1], y_arr[-1]       #location, highest value
        xs, ys = S[-2], y_arr[-2]       #location, second highest
        xm = np.mean(S[0:-1,:],axis=0)  #Centroid of the simplex
        xr = xm + alpha*(xm-xh)         #reflection point 
        yr = f(xr)                  
        nevals+=1; 
        if (nevals == n):
            return S,S[np.argmin(y_arr)]

        if yr < yl:
            xe = xm + beta*(xr-xm)
            ye = f(xe)                
            nevals+=1 
            if (nevals == n):
                return S,S[np.argmin(y_arr)]
            if ye < yr:
                S[-1],y_arr[-1] = xe,ye
            else:
                S[-1],y_arr[-1] = xr,yr
                y_arr[-1] = yr
        elif yr > ys:
            if yr <= yh:
                xh, yh, S[-1], y_arr[-1] = xr, yr, xr, yr

            xc = xm + gamma*(xh - xm)
            yc = f(xc)
            nevals+=1
            if (nevals == n):
                return S,S[np.argmin(y_arr)]

            if yc > yh:
                for i in range(1,len(y_arr)):   #This is intentionally 1, not 0.
                    S[i] = (S[i] + xl)/2
                    y_arr[i] = f(S[i]) 
                    nevals+=1
                    if (nevals == n):
                        return S,S[np.argmin(y_arr)]
            
            else:
                S[-1], y_arr[-1] = xc, yc
        else:
            S[-1], y_arr[-1] = xr, yr

    return S,S[np.argmin(y_arr)]

def optimize(f,num_rivets,neval, nrestarts):
    #f           -> function with emebedded constraitns
    #num_rivets  -> total problem number of rivets (dimension/3 since for each we have x y r)
    #neval -> number of evaluations per restart
    #nrestarts -> number of times to randomly restart
    S = generate_xyr_simplex(num_rivets)
    best = S[0]

    for restart in range(0,nrestarts):
        S,best = nelder_mead(f,S,neval)
        S = generate_xyr_simplex(num_rivets)
        S[0] = best

    return best

def quad_penalty(cs):
    #cs: vector of constraints s.t. c <= 0
    penalty = 0
    for c in cs:
        penalty += max(0,c)**2
    return penalty

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