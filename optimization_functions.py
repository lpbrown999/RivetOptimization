import numpy as np

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
                for i in range(1,len(a)):   #This is intentionally 1, not 0.
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