# toeplitz_decomposition
Applies to code in Steve's GitHub. Written by Aladdin, Visal, Steve. 

### Extracting Data from your binned file ###
To extract binned data, use `extract_realData2.py`, which requires Python 2.7, NumPy, SciPy, and Matplotlib. 

Extract data on CITA (or personal computer for small `n`, `m`), then move the extracted data to SciNet/BGQ.

To extract, use the format:
```
$ python extract_realData2.py binnedDataFile numrows numcols offsetn offsetm n m
```

where `binnedDataFile` is the raw data you wish to extract (must be in the same directory as `extract_realData2.py`). `numrows` is the number of blocks (or the number of frequency bins) and `numcols` is the size of each block (or the number of time bins). `numrows` and `numcols` refer to the raw data, and must be set correctly for proper extraction. The remaining arguments apply to the extracted dynamic spectrum, and can be set as desired. `offsetn` and `offsetm` are the lower bounds of the frequency and time bins, respectively. `n` and `m` are the total number of frequency and time bins (or, equivalently, the number of blocks and the size of each block, respectively)

For example, if your data has `numrows = 16384`, `numcols = 660`, and you want `offsetn = 0`, `offsetm = 0`, `n = 4`, `m = 8`, use:
```
python extract_realData2.py weighted_average_0_1_6.bin 16384 660 0 0 4 8
```

This will create the directory `./processedData/gate0_numblock_4_meff_16_offsetn_0_offsetm_0`

Note that if a directory with this name already exists, the data therein will be overwritten without warning when extract_realData2.py executes. 

The format of the directory name is: `gate0\_numblock\_(n)\_meff\_(mx2)\_offsetn\_(offsetn)\_offsetm\_(offsetm)`

Note that the value of `m` is doubled in the directory name, but you must use the original value of `m` when you perform the decomposition.

Inside this folder, there will be a `gate0_numblock_(n)_meff_(mx2)_offsetn_(offsetn)_offsetm_(offsetm)_toep.npy` file. There will also be `n` npy files. They each represent a block of the Toeplitz matrix. Only the files within this folder are required to perform the decomposition.

There will also be a dat file `gate0_numblock_(n)_meff_(mx2)_offsetn_(offsetn)_offsetm_(offsetm).dat`. This serves an unknown purpose, and the decomposition can be performed without it.

The current version of the code generates a number of png files, and a file `data.tar.gz`. These serve unknown purposes, and the decomposition can be performed without them.

### Performing decomposition ###

##### Local jobs #####

##### Small jobs on BGQ #####

##### Large jobs on BGQ #####


### Plotting results ###

Visal says the module 'reconstruct' in toeplitz_scint.py can be used to plot results. I have not tested this. 

Visal used the program plot_simulated.py to plot results obtained from the decomposition alongside simulated results. This requires a separate calculation of simulated results. I have not tested this.

Aladdin's GitHub repository contains programs plot_simulated.py and plot_real.py, which are not in my repository. I have not tested these.
