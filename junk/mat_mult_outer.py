import sys
import numpy as np
import time
from scipy.linalg.blas import zgeru
import scipy as sp

# Initialize matrices.
n = int(sys.argv[1])
N = int(sys.argv[2])


# Create random matrices (the same ones each time). 
np.random.seed(42)
A_real = np.random.rand(n)-0.5
np.random.seed(43)
A_imaginary = 1.0*np.random.rand(n)-0.5
A = A_real+1.0j*A_imaginary
del A_real
del A_imaginary

np.random.seed(44)
B_real = np.random.rand(n)-0.5
np.random.seed(45)
B_imaginary = np.random.rand(n)-0.5
B = B_real+1.0j*B_imaginary
del B_real
del B_imaginary

# Matrix multiplication.

indices=range(N)

A_2d = A[:,np.newaxis]
B_2d = B[np.newaxis,:]
start_dot = time.time()
for i in indices:
    C = np.dot(A_2d,B_2d)
end_dot = time.time()

start_outer = time.time()
for i in indices:
    D = np.outer(A,B)
end_outer = time.time()

start_ein = time.time()
for i in indices:
    E = np.einsum('i,j->ij', A, B)
end_ein = time.time()

start_spdot = time.time()
for i in indices:
    F = sp.dot(A_2d,B_2d)
end_spdot = time.time()

start_spouter = time.time()
for i in indices:
    G = sp.outer(A, B)
end_spouter = time.time()

start_zgeru = time.time()
for i in indices:
    H = zgeru(1, A, B)
end_zgeru = time.time()

#start_man1 = time.time()
#for i in indices:
#    I = np.empty((n,n),complex)
#    for j in range(n):
#        for k in range(n):
#            G[j,k] = A[j]*B[k]
#end_man1 = time.time()

#start_man2 = time.time()
#for i in indices:
#    J = np.empty((n,n),complex)
#    for k in range(n):
#        for j in range(n):
#            G[j,k] = A[j]*B[k]
#end_man2 = time.time()


print bool(np.array_equal(C,D) and np.array_equal(D,E) and np.array_equal(E,F) and np.array_equal(F,G))
print "Time per multiplication np.dot()  : "+str((end_dot-start_dot)/N)
print "Time per multiplication np.outer(): "+str((end_outer-start_outer)/N)
print "Time per multiplication einsum()  : "+str((end_ein-start_ein)/N)
print "Time per multiplication sp.dot()  : "+str((end_spdot-start_spdot)/N)
print "Time per multiplication sp.outer(): "+str((end_spouter-start_spouter)/N)
print "Time per multiplication zgeru() : "+str((end_zgeru-start_zgeru)/N)
#print "Time per multiplication man1    : "+str((end_man1-start_man1)/N)
#print "Time per multiplication man2    : "+str((end_man2-start_man2)/N)
