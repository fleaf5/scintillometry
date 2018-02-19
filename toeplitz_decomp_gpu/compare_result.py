import os, sys
import numpy as np

A_dir = str(sys.argv[1])
B_dir = str(sys.argv[2])

A = np.load(A_dir)
B = np.load(B_dir)

print "array_equal()       : "+str(np.array_equal(A,B))
rtol=1e-05 # default rtol=1e-05
atol=1e-06  # default atol=1e-08
print "allclose()          : "+str(np.allclose(A, B, rtol=rtol, atol=atol))+" (rtol: "+str(rtol)+", atol: "+str(atol)+")"
"rtol: "+str(rtol)+", atol: "+str(atol)
print "max(abs(real(A-B))) : "+str(np.max(np.absolute(np.real(A-B))))
print "max(abs(imag(A-B))) : "+str(np.max(np.absolute(np.imag(A-B))))

#print "mean(abs(real(A)))  : "+str(np.mean(np.absolute(np.real(A))))
#print "mean(abs(imag(A)))  : "+str(np.mean(np.absolute(np.imag(A))))
#print "mean(abs(real(B)))  : "+str(np.mean(np.absolute(np.real(B))))
#print "mean(abs(imag(B)))  : "+str(np.mean(np.absolute(np.imag(B))))
