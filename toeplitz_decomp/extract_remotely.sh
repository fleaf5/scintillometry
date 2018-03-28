cd /mnt/raid-project/gmrt/dzli/mnt
module load gcc/6.3.0 intel/intel-17 openmpi/2.0.1-intel-17 python/2.7.13-mkl

#python extract_realData3.py binnedDataFile offsetn offsetm n m
dypath=$1
filename=$2
offsetn=$3
offsetm=$4
n=$5
m=$6
echo python extract_realData_npy.py ${dypath}/${filename} $offsetn $offsetm $n $m
python extract_realData_npy.py ${dypath}/${filename} $offsetn $offsetm $n $m

#cat extract_remotely.sh | ssh prawn 
