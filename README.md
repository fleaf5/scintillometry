# toeplitz_decomposition

### Extracting Data from your binned file ###

To extract binned data, use extract_realData2.py

The program extract_realData2.py requires Python 2.7, NumPy, SciPy, and Matplotlib. 

The recommendation is to extract data on personal computer, and then move the extracted data to SciNet/BGQ (extraction on SciNet/BGQ has not been tested).

To extract, use the format:

$ python extract_realData2.py binnedDataFile numofrows numofcolms offsetn offsetm n m

where binnedDataFile is the raw data you wish to extract (must be in the same directory as extract_realData2.py). n is the number of blocks (or the number of frequency bins) and m is the size of each block (or the number of time bins). n and m refer to the size of the raw data, and must be set correctly for proper extraction. The remaining arguments apply to the extracted dynamic spectrum, and can be set to desired values. offsetn and offsetm are the lower bounds of the frequency and time bins, respectively [unverifed]. numofrows 
and numofcolms are the total number of frequency and time bins.

So, for example, if you want numofrows= 2048, numofcols=330, offsetn= 0, offsetm = 140, n=4, m=8, use the call:

python extract_realData2.py gb057_1.input_baseline258_freq_03_pol_all.rebint.1.rebined 2048 330 0 140 4 8

This will create the directory ./processedData/gate0_numblock_4_meff_16_offsetn_0_offsetm_140

Note that if a directory with this name already exists, the data therein will be overwritten without warning when extract_realData2.py executes. 

The format of the directory name is:

gate0\_numblock\_(n)\_meff\_(mx2)\_offsetn\_(offsetn)\_offsetm\_(offsetm)

Note that the value of m is doubled in the directory name, but you must use the original value of m when you perform the decomposition.


### Performing decomposition ###
Proper instructions coming soon.

Refer to https://eor.cita.utoronto.ca/penwiki/User:Sufkes#Successful_trial_decomposition_on_BGQ for an example of a decomposition done on the BGQ.


### Plotting results ###

According to Visal, the module 'reconstruct' in toeplitz_scint.py can be used to plot results. I have not tested this. 

Visal also used the program plot_simulated.py to plot results obtained from the decomposition alongsize simulated results. This requires a separate calculation of simulated results. I have not tested this.

Aladdin's GitHub repository contains programs plot_simulated.py and plot_real.py, which are not in my repository. I have not tested these.

### Description of scripts ###

extract_realData2.py: Splits raw dynamic spectrum into n blocks, saving each in a separate .npy file. 
