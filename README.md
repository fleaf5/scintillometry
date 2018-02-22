# toeplitz_decomposition
Applies to code in Steve's GitHub. Written by Aladdin, Visal, Steve. 

This repository contains two versions of the code: the folder `toeplitz_decomp` contains a double precision, CPU-only version of the code; the folder `toeplitz_decomp_gpu` contains a single-precision version of code which can be run on CPUs only, or can utilize one or more GPUs. 

### Extracting Data from your binned file ###
To extract binned data, use `extract_realData2.py`, which requires Python 2.7, NumPy, SciPy, and Matplotlib. 

Extract data on a CITA machine or your personal computer, then move the extracted data to the system you wish to run the deconvolution routine on.

To extract, use the format:
```
$ python extract_realData2.py binnedDataFile numrows numcols offsetn offsetm n m
```

where *binnedDataFile* is the raw data you wish to extract (must be in the same directory as `extract_realData2.py`). *numrows* and *numcols* refer to the raw data, and must be set correctly for proper extraction. *numrows* is the number of blocks (or the number of frequency bins) and *numcols* is the size of each block (or the number of time bins). The remaining arguments apply to the extracted dynamic spectrum, and can be set as desired. *offsetn* and *offsetm* are the lower bounds of the frequency and time bins, respectively. *n* and *m* are the total number of frequency and time bins desired (or, equivalently, the number of blocks and the size of each block, respectively)

For example, if your data has *numrows* = 16384, *numcols* = 660, and you want *offsetn* = 0, *offsetm* = 0, *n* = 4, *m* = 8, use:
```
python extract_realData2.py weighted_average_0_1_6.bin 16384 660 0 0 4 8
```

This will create the directory `./processedData/gate0_numblock_4_meff_16_offsetn_0_offsetm_0`

Note that if a directory with this name already exists, the data therein will be overwritten without warning when `extract_realData2.py` executes. 

The extraction routine assumes that the input data is of type float32, binary format. If your input data is not a float32 binary file, modify the import step (e.g. change 'float32' to 'float64' in the np.memmap call; or if your data is a NumPy array, change the np.memmap call to np.load).

The format of the directory name is: `gate0_numblock_(n)_meff_(mx2)_offsetn_(offsetn)_offsetm_(offsetm)`

Note that the value of *m* is doubled in the directory name, but you must use the original value of *m* when you perform the decomposition.

Inside this folder, there will be a `gate0_numblock_(n)_meff_(mx2)_offsetn_(offsetn)_offsetm_(offsetm)_toep.npy` file. There will also be *n* npy files. They each represent a block of the Toeplitz matrix. Only the files within this folder are required to perform the decomposition.

### Performing decomposition on BGQ (CPU-only) ###

The decomposition can be performed locally, on SciNet, BGQ, or the SOSCIP GPU cluster. The following instructions are for running the double precision, CPU-only version of the code on the BGQ.

Please refer to SciNet [BGQ wiki](https://wiki.scinet.utoronto.ca/wiki/index.php/BGQ) before continuing.

1. Compress the processed data
```
$ cd processedData/
$ tar -zcvf processedData.tar.gz gate0_numblock_(n)_meff_(mx2)_offsetn_(offsetn)_offsetm_(offsetm)
```

2. Move the compressed folder into BGQ using your login information. For example, using scp:
```
scp processedData.tar.gz (BGQusername)@bgqdev.scinet.utoronto.ca:~/
```

3. ssh into BGQ
```
$ ssh (BGQusername)@bgqdev.scinet.utoronto.ca -X
```

4. Clone the GitHub repository containing the source code:
```
git clone https://github.com/sufkes/scintillometry.git
```

5. Move the compressed data into the folder containing the source code:
```
mv processedData.tar.gz scintillometry/toeplitz_decomp/processedData/
```

6. Copy the source code and the extracted data to your scratch directory:
```
cp -r scintillometry/toeplitz_decomp/ $SCRATCH
```

7. Move to your scratch directory and extract the data:
```
cd $SCRATCH/toeplitz_decomp/processedData/
tar -zxvf processedData.tar.gz
cd ..
```

8. Write/edit a job script per the instructions below.

##### Submitting small jobs (using debugjob) #####
9. Copy the template job script `jobscript_bgq_debugjob.sh` to a new name:
```
cp jobscript_bgq_debugjob.sh smalljob_name.sh
```

10. Edit the copy `smalljob_name.sh` (e.g. with emacs, vi).
* *method* is the decomposition scheme. yty2 is the method used in Nilou's report.
* Set parameters *offsetn*, *offsetm*, *n* and *m* to the values that were used in `extract_realData2.py`. 
* *p* is an integer parameter used in the decomposition (function currently unclear). It can be set to 2*m*, *m*, *m*/2, *m*/4. Fastest results reportedly occur for *p = m*/2 or *p = m*/4. 
* *pad* is a Boolean value which specifies whether or not to use padding (1 or 0).

* *bg_size* is the number of nodes in the block. This is automatically set to 64 in a debugjob.
* *NP* is the number of MPI processes. **It must be set to 2*n*.**
* *RPN* is the number of MPI processes per node.
* *OMP_NUM_THREADS* is the number of OpenMP threads per MPI process.

The following conditions must hold for the run to execute:
* *NP* = 2*n*
* *NP* ≤ (*RPN* * *bg_size*)
* *RPN* ≤ *NP*
* (*RPN* * *OMP_NUM_THREADS*) ≤ 64 = number of threads per node.

11. Request a debug block:
```
debugjob
```

12. Once inside the debug block, execute the job script:
```
./smalljob_name.sh
```

The run is timed using the `time` function. Execution consists of 2*n* - 1 loops. Results are saved in `./results/`

12. Move results from scratch directory to desired location.

Results are stored in `./results/gate0_numblock_(n)_meff_(mx2)_offsetn_(offsetn)_offsetm_(offsetm)_uc.npy`.

##### Submitting large jobs (using llsubmit) #####

9. Copy the template job script `jobscript_bgq_large.sh` to a new name:
```
cp jobscript_bgq_large.sh largejob_name.sh
```

10. Edit the copy `largejob_name.sh`.
* Follow the same instructions as for small jobs.
* The number of nodes must be specified. *bg_size* = 64, 128, 256, 512, 1024, 2048.
* Set *sourcedir* to the directory of the source code.

11. Submit the job:
```
llsubmit ./largejob_name.sh
```

See SciNet [BGQ wiki](https://wiki.scinet.utoronto.ca/wiki/index.php/BGQ) for instructions on monitoring progress.

12. Move results from scratch directory to desired location.

Results are stored in `./results/gate0_numblock_(n)_meff_(mx2)_offsetn_(offsetn)_offsetm_(offsetm)_uc.npy`.

### Performing decomposition on the SOSCIP GPU cluster ###
Please refer to SciNet [SOSCIP GPU wiki](https://wiki.scinet.utoronto.ca/wiki/index.php/SOSCIP_GPU) before continuing.

To run the GPU version of the code on the SOSCIP GPU cluster, follow steps 1-8 for running the CPU-only version of the code on the BGQ, instead using the scripts in the `toeplitz_decomp_gpu` folder.

9. Copy the template job script `jobscript_soscip_gpu.sh` to a new name:
```
cp jobscript_soscip_gpu.sh gpujob_name.sh
```

10. Edit the copy `gpujob_name.sh` (e.g. with emacs, vi).
* The parameters have the same meaning as in the BGQ debugjob job script described above.
* *--nodes* specifies the number of compute nodes to use. Each node has 2x10x8=160 CPU threads and 4 GPUs. 
* *--ntasks* specifies the number of MPI processes. This must be set to 2*n*.
* *--time* specifies the wall clock limit.
* *--gres=gpu:4* specifies to use 4 GPUs per node.
* *PYTHON* specifies the copy of Python to be used. The default Python installation on the SOSCIP GPU cluster cannot run the GPU version of the code, as ArrayFire is not installed on it.
* *SCRIPT* specifies the path of the Python script to run. 

11. To select whether or not to use the GPUs, set the parameters *use_gpu_Om2* and *use_gpu_Om3* in `new_factorize_parallel.py` to True or False. If *use_gpu_Om2* = True, all O(m^2) matrix operations will be performed on GPUs; if *use_gpu_Om3* = True, all O(m^3) matrix operations will be performed on GPUs. It appears that the best performance is acheived when *use_gpu_Om2* = False, and *use_gpu_Om3* = True.

12. Submit the job:
```
sbatch gpujob_name.sh
```

13. Move results from scratch directory to desired location.

Results are stored in `./results/gate0_numblock_(n)_meff_(mx2)_offsetn_(offsetn)_offsetm_(offsetm)_uc.npy`.

### Interpreting the output ###

The file `./results/gate0_numblock_(n)_meff_(mx2)_offsetn_(offsetn)_offsetm_(offsetm)_uc.npy` is a 1D NumPy array containing the flattened electric field in Fourier space. To convert this file to a 2D array, use the script `unflatten_E.py`. The correct way to reconstruct the electric field from the output of our deconvolution routine is unknown. `unflatten_E.py` gets us as close to the correct result as we know how to. 
