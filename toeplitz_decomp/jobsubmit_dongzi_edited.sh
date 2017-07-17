#!/bin/sh
method=yty2					# Scheme of decomposition. yty2 is the method described in Nilou's report.
offsetn=0
offsetm=0
n=128
m=128
p=64							# VISAL SAYS: Can set to m/4, m/2, m, 2m. Fastest when set to m/2 or m/4.
pad=1						# 0 for no padding; 1 for padding.

# bg_size = 64 is the number of nodes in the block (always 64 in debugjob).
NP=256						# Number of MPI processes. Must be set to 2n for this code. NP <= (RPN * bg_size)
RPN=8						# Number of MPI processes per node = 1,2,4,8,16,32,64. RPN <= NP

module purge
module unload mpich2/xl
source /scratch/s/scinet/nolta/venv-numpy/bin/activate
module load python/2.7.3 xlf/14.1 essl/5.1 bgqgcc/4.8.1
module load binutils/2.23 mpich2/gcc-4.8.1 
export OMP_NUM_THREADS=8

time runjob --np ${NP} --ranks-per-node=${RPN} --envs HOME=$HOME LD_LIBRARY_PATH=/scinet/bgq/Libraries/HDF5-1.8.12/mpich2-gcc4.8.1//lib:/scinet/bgq/Libraries/fftw-3.3.4-gcc4.8.1/lib:/scinet/bgq/tools/binutils-2.23/lib64:/scinet/bgq/tools/Python/python2.7.3-20131205//lib:/opt/ibmcmp/lib64/bg/bglib64/:/bgsys/drivers/ppcfloor/gnu-linux/powerpc64-bgq-linux/lib/:/opt/ibmcmp/xlf/bg/14.1/bglib64:/opt/ibmmath/essl/5.1/lib64:$LD_LIBRARY_PATH PYTHONPATH=/scinet/bgq/tools/Python/python2.7.3-20131205/lib/python2.7/site-packages/ : `which python` run_real_new.py yty2 ${offn} ${offm} ${n} ${m} ${p} 1
#PYTHONPATH=/scinet/bgq/tools/Python/python2.7.3-20131205/lib/python2.7/site-packages/: \
