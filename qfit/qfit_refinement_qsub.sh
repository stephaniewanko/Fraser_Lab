#PBS -t 1-1
#PBS -l walltime=100:00:00
#PBS -l nodes=1
#PBS -l mppnppn=1


#this script will run qfit based on the input PDB names you have.

#________________________________________________INPUTS________________________________________________#
working_dir='/data/wankowicz/190815_qfit_done/'  #where the folders are located
PDB_file=/mnt/home1/wankowicz/190709_qfit/gm.txt #list of PDB IDs
echo $working_dir
export OMP_NUM_THREADS=1

#________________________________________________SET PATHS________________________________________________#
source /home/wankowicz/phenix-installer-1.16-3546-intel-linux-2.6-x86_64-centos6/phenix-1.16-3546/phenix_env.sh
export PATH="/home/wankowicz/anaconda3/bin:$PATH"
source activate qfit2.1
which python

#________________________________________________CHECK VARIABLES________________________________________________#
echo 'which job:'
echo $PBS_JOBID
echo $PBS_ARRAYID

echo "I ran on:"
cat $PBS_NODEFILE


#________________________________________________RUN QFIT________________________________________________#
#PDB=$(cat $PDB_file | head -n $LSB_JOBINDEX | tail -n 1)
PDB=$(cat $PDB_file | head -n $PBS_ARRAYID | tail -n 1)
echo $PDB
cd $working_dir
echo 'should be:'
echo $PWD

cd $PDB

#cd /tmp
#ls
#mkdir wankowicz
#cd wankowicz

#cp -R ${working_dir}/${PDB}/ /tmp/wankowicz/
#cd ${PDB}

echo 'PWD':
echo $PWD

echo 'here'
if [[ -e ${PDB}_qFit.pdb ]]; then
   echo 'Refinement Done'
else
   #sh /mnt/home1/wankowicz/scripts/fixing_fuckup_refinement.sh $PDB
   sh /mnt/home1/wankowicz/scripts/qfit_post_refine_script_test.sh $PDB
   #sh /mnt/home1/wankowicz/scripts/qfit_pre_refine_script.sh $PDB
fi

if [[ -e ${PDB}_single_conf.pdb ]];
   echo 'Single Conf Refinement Done'
else
   sh /mnt/home1/wankowicz/scripts/qfit_pre_refine_script.sh $PDB
fi

cp -R /tmp/wankowicz/$PDB/ $working_dir/
#echo 'here2'
