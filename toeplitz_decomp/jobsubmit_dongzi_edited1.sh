#!/bin/sh

method=yty2
offn=0
offm=0
n=128
m=128
p=64

NP=256
RPN=8
module purge
module unload mpich2/xl
source /scratch/s/scinet/nolta/venv-numpy/bin/activate
module load python/2.7.3 xlf/14.1 essl/5.1 bgqgcc/4.8.1
module load binutils/2.23 mpich2/gcc-4.8.1 
export OMP_NUM_THREADS=8

time runjob --np ${NP} --ranks-per-node=${RPN} --envs HOME=$HOME LD_LIBRARY_PATH=/scinet/bgq/Libraries/HDF5-1.8.12/mpich2-gcc4.8.1//lib:/scinet/bgq/Libraries/fftw-3.3.4-gcc4.8.1/lib:/scinet/bgq/tools/binutils-2.23/lib64:/scinet/bgq/tools/Python/python2.7.3-20131205//lib:/opt/ibmcmp/lib64/bg/bglib64/:/bgsys/drivers/ppcfloor/gnu-linux/powerpc64-bgq-linux/lib/:/opt/ibmcmp/xlf/bg/14.1/bglib64:/opt/ibmmath/essl/5.1/lib64:$LD_LIBRARY_PATH PYTHONPATH=/scinet/bgq/tools/Python/python2.7.3-20131205/lib/python2.7/site-packages/ : `which python` run_real_new.py ${method} ${offn} ${offm} ${n} ${m} ${p} 1
#PYTHONPATH=/scinet/bgq/tools/Python/python2.7.3-20131205/lib/python2.7/site-packages/: \
