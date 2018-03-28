SHELL:=/bin/bash

dypath=/mnt/raid-project/gmrt/dzli/vela760/LBA/data
filename=I_late_tbin8192_middle_fbin6144_aftersvd.npy 
offsetn=0
offsetm=0
n=8192
m=512

.PHONY:extract
extract:
	./extract_remotely.sh ${dypath} ${filename} ${offsetn} ${offsetm} $n $m 

.PHONY:output
output:
	./output.sh ${dypath} ${filename} ${offsetn} ${offsetm} $n $m 
