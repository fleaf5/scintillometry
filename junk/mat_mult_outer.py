import sys
import numpy as np
import time

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

print bool(np.array_equal(C,D) and np.array_equal(D,E))
print "Time per multiplication dot()   : "+str((end_dot-start_dot)/N)
print "Time per multiplication outer() : "+str((end_outer-start_outer)/N)
print "Time per multiplication einsum(): "+str((end_ein-start_ein)/N)

