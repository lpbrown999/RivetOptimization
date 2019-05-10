import numpy as np
from main import nelder_mead


def rosenbrock(x):
	return 100*(x[1]-x[0])**2 + (1-x[0])**2

ndim = 2
S = np.random.random_sample((ndim+1,ndim))
neval = 100

S,x = nelder_mead(rosenbrock,S,neval)
print(S)
print(x)
print(rosenbrock(x))