import numpy as np
import math
import configparser

def generate_n_x_y_r_simplex():
	
	config = configparser.ConfigParser()
	config.read('optimization_config.ini')

	xmin = 0
	xmax = float(config['CellGeometry']['cellL'])
	ymin = 0
	ymax = float(config['CellGeometry']['cellW'])
	rmin = 0
	rmax = xmax/4
	nmin = int(float(config['Optimization']['min_num_rivets']))
	nmax = int(float(config['Optimization']['max_num_rivets']))

	ndim = nmax*3 + 1
	S = np.zeros((ndim+1,ndim))
	#First column is number of rivets
	S[:,0] = np.random.randint(nmin,nmax+1,ndim+1)

	#Now do the xs,ys,rs. 
	S[:,1::3] = np.random.uniform(xmin,xmax,(ndim+1,nmax))
	S[:,2::3] = np.random.uniform(ymin,ymax,(ndim+1,nmax))
	S[:,3::3] = np.random.uniform(rmin,rmax,(ndim+1,nmax))
	
	return S

#Unconstrained optimization method nelder mead-simplex!
def nelder_mead(f, S, n, alpha=1.0, beta=2.0, gamma=0.5):
	#f -> function 
	#S -> Initial simplex. ndim+1 points by ndim dimensions.
	#n -> allowed evaluations
	nevals, y_arr = len(S), np.array(list(map(f,S)))

	while nevals < n:
		print("\nNelder mead num_evals: %s" % nevals)

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

def optimize(f, S_gen, neval, nrestarts, penalty, penalty_growth):
	#f      -> function with emebedded constraints.
	#		   must have signature f(inputvector, penalty weight)
	#S_gen  -> function that returns a simplex of the appropriate size.
	#neval -> number of evaluations per restart
	#nrestarts -> number of times to randomly restart
	#penalty -> initial constraint penalty
	#penalty_growth -> number to multiply penalty by every time we restart
	
	S = S_gen()
	best = S[0]
	counter = 0
	for restart in range(0,nrestarts+1):
		f_penalized = lambda inpvec: f(inpvec,penalty)
		S,best = nelder_mead(f_penalized,S,int(neval/(nrestarts+1)))
		S = S_gen()
		S[0] = best
		penalty *= penalty_growth

	return best

def quad_penalty(cs,p):
	#cs: vector of constraints s.t. c <= 0
	penalty = 0
	for c in cs:
		penalty += max(0,c)**2
	return p*penalty
