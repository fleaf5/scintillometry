import sys
import numpy as np
import scipy as sp
from scipy import linalg
import numpy.linalg
import os
import mmap
#from scipy.fftpack import fftshift, fft2, ifft2, ifftshift

filename = str(sys.argv[1])
num_rows=int(sys.argv[2]) # frequency
num_columns=int(sys.argv[3]) # time
offsetn=int(sys.argv[4]) # offset in freq
offsetm=int(sys.argv[5]) # offset in time
sizen=int(sys.argv[6]) # size of freq = n
sizem=int(sys.argv[7]) # size of time = m
nump=sizen

build_Inm = False # Select whether to build the Block Toeplitz matrix Inm, and compute its Cholesky factor (sizes 4nm x 4nm). Requires small n, m.


if offsetn>num_rows or offsetm>num_columns or offsetn+sizen>num_rows or offsetm+sizem>num_columns:
	print ("Error sizes or offsets don't match")
	sys.exit(1)

## Load dynamic spectrum I(f,t). Edit this line according to file format. 
a = np.memmap(sys.argv[1], dtype='float32', mode='r', shape=(num_rows,num_columns),order='F')
#a = np.load(filename).real

## Choose region of frequency and time.
print "Choosing region of frequency and time."
a = a[offsetn:offsetn+sizen, offsetm:offsetm+sizem]

## Set constants.
pad=1
pad2=1

neff=sizen+sizen*pad
meff=sizem+sizem*pad

meff_f=meff+pad2*meff

## Zero pad. 
print "Zero padding."
a_input=np.zeros(shape=(neff,meff), dtype=complex)
a_input[:sizen,:sizem]=np.copy(a)

## Specify file directories.
newdir = "gate0_numblock_%s_meff_%s_offsetn_%s_offsetm_%s" %(str(sizen),str(meff_f/2),str(offsetn),str(offsetm))
if not os.path.exists("processedData/"+newdir):	
	os.makedirs("processedData/"+newdir)

const=int(pad2*meff/2)

## Ensure positive definite matrix.
print "Square rooting."
a_input=np.sqrt(a_input)

print "Computing first Fourier transfrom"
a_input[:sizen,:sizem]=np.fft.fft2(a_input,s=(sizen,sizem))

print "Shifting blocks."
a_input[0:sizen, meff-int(round(sizem/2.)):meff] =  a_input[0:sizen, int(sizem/2 + 0.5):sizem]
a_input[0:sizen, int(round(sizem/2.)):sizem] = 0+0j

a_input[neff-int(round(sizen/2.)):neff,0:meff] = a_input[int(sizen/2+0.5):sizen, 0:meff]
a_input[int(round(sizen/2.)):sizen, 0:meff] = 0+0j

## Inverse Fourier transform 
print "Computing inverse Fourier transform."
a_input=np.fft.ifft2(a_input,s=(neff,meff))

print "Squaring."
a_input=np.power(np.abs(a_input),2)

print "Computing second Fourier transform."
a_input=np.fft.fft2(a_input,s=(neff,meff))

path="processedData/gate0_numblock_%s_meff_%s_offsetn_%s_offsetm_%s" %(str(sizen),str(meff_f/2),str(offsetn),str(offsetm))
mkdir="mkdir "+path

epsilon=np.identity(int(meff_f/2))  *1e-7

if build_Inm:
    normal_blocks = np.zeros((2*sizem, 2*sizen*2*sizem),complex)
    Inm = np.zeros((2*sizen*2*sizem, 2*sizen*2*sizem),complex)

## Make blocked toeplitz elements.
print "Making blocked Toeplitz elements and saving them."
if neff == 1:
    neff += 1
for j in np.arange(0,int(neff/2)):
    print '{:.2f}'.format(float(j)/(float(neff)/2)*100)+"% complete\r",
    sys.stdout.flush()
    rows = np.append(a_input[j,:meff-const], np.zeros(pad2*meff*0+const))
    cols = np.append(np.append(a_input[j,0], a_input[j,const+1:][::-1]), np.zeros(pad2*meff*0+const))
    file_name=path+'/'+str(j)+".npy"
    toep_block = np.conj(sp.linalg.toeplitz(cols,rows)).T
    np.save(file_name, toep_block.astype('complex64'))
    if j==0:
        toep_block = np.conj(sp.linalg.toeplitz(np.conj(np.append(a_input[j,:meff-const],np.zeros(pad2*meff*0+const))))+epsilon).T
        np.save(file_name, toep_block.astype('complex64'))
    if build_Inm:
        normal_blocks[0:meff, j*meff:(j+1)*meff] = np.conj(toep_block.T) # undo conjugate transpose to get original blocks.
print '{:.2f}'.format(100)+"% complete\r"
# The extraction is complete at this point. The remaining code is only executed if you select to construct the block Toeplitz matrix Inm.

# Build the block Toeplitz matrix Inm.
if build_Inm:
    print "Making block Toeplitz matrix Inm."
    for j in range(2*sizen):
        Inm[j*meff:(j+1)*meff, j*meff:] = normal_blocks[:, :(2*sizen-j)*meff]

    for i in range(2*sizen*meff):
        for j in range(2*sizen*meff):
            if i > j:
                Inm[i,j] = np.conj(Inm[j,i])

    # Save block Toeplitz matrix Inm.
    if not os.path.exists("results/"+newdir):	
	    os.makedirs("results/"+newdir)
    result_path="results/gate0_numblock_%s_meff_%s_offsetn_%s_offsetm_%s" %(str(sizen),str(meff_f/2),str(offsetn),str(offsetm))
    np.save(result_path+'/Inm_input.npy',Inm) # Block Toeplitz matrix Inm.

    # Check if blocked Toeplitz matrix is Hermitian.
    hermitian = np.allclose(Inm,np.conj(Inm.T))
    print "Inm Hermitian: "+str(hermitian)

    # Check if blocked Toeplitz matrix is positive definite. 
    w, v = np.linalg.eig(Inm)
    pos_def = True 
    for evalue in w:
        if evalue <= 0.0:
            pos_def = False
            break
    print "Inm Positive definite: "+str(pos_def)
    
    # Compute and save the Cholesky factor of Inm.
    print "Computing Cholesky factor of Inm."
    L = np.linalg.cholesky(Inm) # Lower triangular Cholesky factor. 
    np.save(result_path+'/L_input.npy',L)
