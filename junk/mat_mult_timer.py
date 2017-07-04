import time
import numpy as np

# Initialize matrices.
n = 1000
m = 1000

# Create random matrices (the same ones each time). 
np.random.seed(42)
A = np.random.rand(n,m)-0.5

np.random.seed(43)
B = np.random.rand(m,n)-0.5

# Time matrix multiplication.
tic = time.clock()

C = np.dot(A,B)

toc = time.clock()

mult_time = toc - tic

print "({}, {}):".format(n, m), "{:.4E}".format(mult_time),"s"


