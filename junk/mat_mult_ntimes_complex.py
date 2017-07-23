import sys
import numpy as np
import time

# Initialize matrices.
n = int(sys.argv[1])
N = int(sys.argv[3])
m = n

# Create random matrices (the same ones each time). 
np.random.seed(42)
A_real = np.random.rand(n,m)-0.5
np.random.seed(43)
A_complex = 1.0j*np.random.rand(n,m)-0.5j

np.random.seed(44)
B_real = np.random.rand(m,n)-0.5
np.random.seed(45)
B_complex = 1.0j*np.random.rand(m,n)-0.5j

# Matrix multiplication.

indices=range(N)
start = time.time()
for i in indices:
    C = np.dot(A,B)
end = time.time()

print "Total time: "+str(end-start)
print "Time per multiplication: "+str((end-start)/N)
