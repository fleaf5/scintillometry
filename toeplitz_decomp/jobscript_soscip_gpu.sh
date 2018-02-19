#!/bin/bash
#SBATCH --nodes=1   # 1 node = 20 CPU cores + 4 GPUs
#SBATCH --ntasks=8  # 8 threads per core; 8*20=160 threads per node. Must be set to 2n. 
#SBATCH --time=00:10:00
#SBATCH --gres=gpu:4

# Specify parameters for deconvolution routine.
method=yty2
offsetn=0
offsetm=0
n=4
m=4
p=8
pad=1

# Specify location of Python and script.
PYTHON=/home/a/aparamek/sufkes/anaconda2/bin/python2
SCRIPT=/scratch/a/aparamek/sufkes/scintillometry/toeplitz_decomp/run_real_new.py

# Submit deconvolution job.
cd $SLURM_SUBMIT_DIR
time srun $PYTHON $SCRIPT $method $offsetn $offsetm $n $m $p $pad # number of tasks to run is specified above.
