import sys
import numpy as np
from scipy.linalg.blas import zgemm
import time

# Initialize matrices.
n = int(sys.argv[1]) # Rows in matrix
k = int(sys.argv[2])
m = int(sys.argv[3]) # Columns in matrix
N = int(sys.argv[4]) # Number of repetitions to average over

# Create random matrix (the same one each time). 
np.random.seed(42)
C_real = np.random.rand(n+10,m)-0.5
np.random.seed(43)
C_imaginary = 1.0*np.random.rand(n+10,m)-0.5
C = C_real+1.0j*C_imaginary

np.random.seed(44)
A_real = np.random.rand(n,k)-0.5
np.random.seed(45)
A_imaginary = 1.0*np.random.rand(n,k)-0.5
A = A_real+1.0j*A_imaginary

np.random.seed(46)
B_real = np.random.rand(k,m)-0.5
np.random.seed(47)
B_imaginary = 1.0*np.random.rand(k,m)-0.5
B = B_real+1.0j*B_imaginary

alpha = 1.0
beta  = 1.0

start = 4
end = 4 + n

indices=range(N) # list to loop over.

times_dot = np.empty(N)
for i in indices:
    start_dot = time.time()
    C[start:end,:] = C[start:end,:] + A.dot(B)
    end_dot = time.time()
    times_dot[i] = end_dot - start_dot
C_dot = C
C = C_real+1.0j*C_imaginary


times_zgemm = np.empty(N)
for i in indices:
    start_zgemm = time.time()
    C[start:end,:] = zgemm(alpha=1.0, a=B.T, b=A.T, beta=1.0, c=C.T[:,start:end]).T
    end_zgemm = time.time()
    times_zgemm[i] = end_zgemm - start_zgemm
C_zgemm = C
C = C_real+1.0j*C_imaginary

print "Equal: "+str(bool(np.allclose(C_dot,C_zgemm)))
print "\ndot():"
print "min  = "+str(times_dot.min())
print "max  = "+str(times_dot.max())
print "mean = "+str(times_dot.mean())
print "\nzgemm(A):"
print "min  = "+str(times_zgemm.min())
print "max  = "+str(times_zgemm.max())
print "mean = "+str(times_zgemm.mean())
