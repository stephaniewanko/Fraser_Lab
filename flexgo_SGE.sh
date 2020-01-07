#!/bin/bash

#$ -l h_vmem=80G
#$ -l mem_free=64G
#$ -t 1-1
#$ -l h_rt=100:00:00
#$ -pe smp 2
#$ -R yes
#$ -V

#________________________________________________INPUTS________________________________________________#
input_file=/wynton/home/fraserlab/swankowicz/20190708_Ens_Paper/PDB_ids.txt
base_dir='/wynton/group/fraser/swankowicz/new_phenix/'

#________________________________________________Activate Env________________________________________________#
source /wynton/home/fraserlab/swankowicz/phenix-installer-dev-3594-intel-linux-2.6-x86_64-centos6/phenix-dev-3594/phenix_env.sh
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate phenix_ens
which python

#________________________________________________RUN PHENIX________________________________________________#
PDB='3rze' #$(cat $input_file | head -n $SGE_TASK_ID | tail -n 1)
echo 'PDB'
echo $PDB
cd $base_dir
cd $PDB


#____________________________________________MOVING TO SCRATCH_____________________________________________#
echo $PWD

/wynton/home/fraserlab/swankowicz/flexgeo/FleXgeo/bin/FleXgeo_ARCHLinux -pdb=${PDB}_1_10_2/${PDB}_1_10_2.pdb -ncpus=2
