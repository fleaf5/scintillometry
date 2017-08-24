import sys
import numpy as np
from scipy.linalg.blas import zdotc
import time
from copy import deepcopy

# Initialize matrices.
n = int(sys.argv[1]) # Rows in matrix
N = int(sys.argv[2]) # Number of repetitions to average over

# Create random matrix (the same one each time). 
np.random.seed(42)
x_real = np.random.rand(n)-0.5
np.random.seed(43)
x_imaginary = 1.0*np.random.rand(n)-0.5
x = x_real+1.0j*x_imaginary

np.random.seed(44)
y_real = np.random.rand(n)-0.5
np.random.seed(45)
y_imaginary = 1.0*np.random.rand(n)-0.5
y = y_real+1.0j*y_imaginary

indices=range(N) # list to loop over.

#b.getA2().dot(np.conj(X2.T))

times_dot = np.empty(N)
for i in indices:
    start_dot = time.time()
    C = x.dot(np.conj(y))
    end_dot = time.time()
    times_dot[i] = end_dot - start_dot
C_dot = deepcopy(C)


print x.T.flags['F_CONTIGUOUS']
print y.T.flags['F_CONTIGUOUS']
times_zdotc= np.empty(N)
for i in indices:
    start_zdotc = time.time()
    C = zdotc(y.T, x.T)
    end_zdotc = time.time()
    times_zdotc[i] = end_zdotc - start_zdotc
C_zdotc = deepcopy(C)


print "Equal: "+str(bool(np.allclose(C_dot,C_zdotc)))
print "\ndot():"
print "min  = "+str(times_dot.min())
print "max  = "+str(times_dot.max())
print "mean = "+str(times_dot.mean())
print "\zdotc(A):"
print "min  = "+str(times_zdotc.min())
print "max  = "+str(times_zdotc.max())
print "mean = "+str(times_zdotc.mean())
