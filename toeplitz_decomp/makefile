SHELL:=/bin/bash

dypath=/mnt/raid-project/gmrt/dzli/vela760/LBA/data
filename=I_AtPa_IF0_fbin4096_tbin512_fbin1_tbin2.npy 
offsetn=0
offsetm=0
n=4096
m=512

.PHONY:extract
extract:
	./extract_remotely.sh ${dypath} ${filename} ${offsetn} ${offsetm} $n $m 

rsync_forward:
	module load hpnssh; ssh -V;\
	extract_path=/mnt/raid-project/gmrt/dzli/toe;\
	bgq_path=/scratch/p/pen/fleaf5/scintillometry/toeplitz_decomp;\
	nohup rsync -vrtlD -e "ssh" nuexport:$${extract_path}/processedData $${bgq_path}/ > log_rsync 2>&1 &

rsync_back:
	module load hpnssh; ssh -V;\
	bgq_path=/scratch/p/pen/fleaf5/scintillometry/toeplitz_decomp;\
	echo ${dypath}
	nohup rsync -vrtlD -e "ssh" $${bgq_path}/results/E_tilde* nuexport:$${dypath} > log_rsync 2>&1 &

.PHONY:output
output:
	./output.sh ${dypath} ${filename} ${offsetn} ${offsetm} $n $m 
