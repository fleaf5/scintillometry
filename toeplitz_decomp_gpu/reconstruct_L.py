# This script can be used to reconstruct the Cholesky factor after decomposing with our code. To reconstruct the Cholesky factor, you must set detailSave=True in run_real_new.py. 

import os, sys
import numpy as np

offsetn     = int(sys.argv[1])
offsetm     = int(sys.argv[2])
n           = int(sys.argv[3])
m           = int(sys.argv[4])
meff = 2*m
result_dir="results/gate0_numblock_%s_meff_%s_offsetn_%s_offsetm_%s" %(str(n),str(meff),str(offsetn),str(offsetm)) # path to folder containing L_0-0.npy, L_0-1.npy etc.

L_result = np.zeros((2*n*meff,2*n*meff), complex)

for i in range(2*n):
    for j in range(2*n): 
        path = result_dir+"/L_"+str(i)+"-"+str(j)+".npy"
        
        if os.path.isfile(path):
            Ltemp = np.load(path)
            L_result[2*m*j: 2*m*(j + 1), 2*m*i:2*m*(i + 1)] = Ltemp


# L_result is the complete Cholesky factor.
np.save(result_dir+'/L_result.npy',L_result) # Block Toeplitz matrix Inm.

