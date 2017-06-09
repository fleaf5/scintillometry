#!/bin/sh
source /scratch/s/scinet/nolta/venv-numpy/setup
module purge
module unload mpich2/xl
module load binutils/2.23 bgqgcc/4.8.1 mpich2/gcc-4.8.1
module load python/2.7.3
export OMP_NUM_THREADS=8	# Used in Visal's jobsubmit.h
NP=8   				# VISAL SAYS: must be set to 2n 
OMP=8				# ALADDIN SAYS: (RPM * OMP) ≤ 64
RPN=8
n=4
m=4
p=2
time runjob --np ${NP} --ranks-per-node=${RPN} --envs HOME=$HOME LD_LIBRARY_PATH=/scinet/bgq/Libraries/HDF5-1.8.12/mpich2-gcc4.8.1//lib:/scinet/bgq/Libraries/fftw-3.3.4-gcc4.8.1/lib:$LD_LIBRARY_PATH PYTHONPATH=/scinet/bgq/tools/Python/python2.7.3-20131205/lib/python2.7/site-packages/ : /scratch/s/scinet/nolta/venv-numpy/bin/python run_real_new.py yty2 0 0 ${n} ${m} ${p} 1