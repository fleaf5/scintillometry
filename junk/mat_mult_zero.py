import sys
import numpy as np

# Initialize matrices.
n = int(sys.argv[1])
if len(sys.argv) == 3:
	m = int(sys.argv[2])
else:
	m = n

# Create random matrices (the same ones each time). 
np.random.seed(42)
A = np.random.rand(n,m)-0.5

np.random.seed(43)
B = np.random.rand(m,n)-0.5
