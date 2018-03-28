cd /mnt/raid-project/gmrt/dzli/mnt
module load gcc/6.3.0 intel/intel-17 openmpi/2.0.1-intel-17 python/2.7.13-mkl

dypath=$1
filename=$2
offsetn=$3
offsetm=$4
n=$5
m=$6
meff=$(($m*2))
echo python unflatten_E.py ${offsetn} ${offsetm} ${n} ${m}

python unflatten_E.py ${offsetn} ${offsetm} ${n} ${m}
outfilename=${filename//'.npy'/_numblock_${n}_meff_${meff}_offsetn_${offsetn}_offsetm_${offsetm}}
#mv gate0_numblock_${n}_meff_${meff}_offsetn_${offsetn}_offsetm_${offsetm}}/E_tilde.npy ${outfilename}.npy
#cat extract_remotely.sh | ssh prawn 
