import sys
import numpy as np
import scipy as sp
from scipy import linalg
import os	
import mmap
from scipy.fftpack import fftshift, fft2, ifft2, ifftshift

filename = str(sys.argv[1])
num_rows=int(sys.argv[2]) # frequency
num_columns=int(sys.argv[3]) # time
offsetn=int(sys.argv[4]) # offset in freq
offsetm=int(sys.argv[5]) # offset in time
sizen=int(sys.argv[6]) # size of freq = n
sizem=int(sys.argv[7]) # size of time = m
nump=sizen

if offsetn>num_rows or offsetm>num_columns or offsetn+sizen>num_rows or offsetm+sizem>num_columns:
	print ("Error sizes or offsets don't match")
	sys.exit(1)

## Load dynamic spectrum I(f,t). Edit this line according to file format. 
a = np.memmap(sys.argv[1], dtype='float32', mode='r', shape=(num_rows,num_columns),order='F')
#a = np.load(filename).real

## Set constants.
pad=1
pad2=1

neff=sizen+sizen*pad
meff=sizem+sizem*pad

meff_f=meff+pad2*meff

## Select region of data and zero pad. 
print "Zero padding."
a_input=np.zeros(shape=(neff,meff), dtype=complex)
a_input[:sizen,:sizem]=np.copy(a[offsetn:offsetn+sizen,offsetm:offsetm+sizem])

## Specify file directories.
newdir = "gate0_numblock_%s_meff_%s_offsetn_%s_offsetm_%s" %(str(sizen),str(meff_f/2),str(offsetn),str(offsetm))
if not os.path.exists("processedData/"+newdir):	
	os.makedirs("processedData/"+newdir)

const=int(pad2*meff/2)

## Ensure positive definite matrix.
print "Square rooting."
a_input=np.sqrt(a_input)

print "Computing first Fourier transform"
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
    np.save(file_name, np.conj(sp.linalg.toeplitz(cols,rows)).T.astype('complex64'))
    if j==0:
        np.save(file_name, np.conj(sp.linalg.toeplitz(np.conj(np.append(a_input[j,:meff-const],np.zeros(pad2*meff*0+const))))+epsilon).T.astype('complex64'))
    
