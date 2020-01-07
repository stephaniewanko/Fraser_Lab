#!/bin/bash

#$ -l h_vmem=80G
#$ -l mem_free=64G
#$ -t 1-5
#$ -l h_rt=100:00:00
#$ -pe smp 2
#$ -R yes
#$ -V

#________________________________________________INPUTS________________________________________________#
input_file=/wynton/home/fraserlab/swankowicz/20190708_Ens_Paper/other_paper/PDB_ids.txt #list of PDB names
base_dir='/wynton/home/fraserlab/swankowicz/20190708_Ens_Paper/amber_refinement/' #location of folders with PDB files
export OMP_NUM_THREADS=1

#________________________________________________Activate Env________________________________________________#
echo 'nslots'
echo $NSLOTS
echo 'sge':
echo $SGE_TASK_ID
#source /wynton/home/fraserlab/swankowicz/phenix-1.15.2-3472/phenix_env.sh
source /wynton/home/fraserlab/swankowicz/phenix-1.8.2-1309/phenix_env.sh
#source /wynton/home/fraserlab/swankowicz/phenix-installer-dev-3580-intel-linux-2.6-x86_64-centos6/phenix-dev-3580/phenix_env.sh
#source /wynton/home/fraserlab/swankowicz/phenix-installer-dev-3594-intel-linux-2.6-x86_64-centos6/phenix-dev-3594/phenix_env.sh
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate phenix_ens
which python

#________________________________________________RUN PHENIX________________________________________________#

PDB = $(cat $input_file | head -n $SGE_TASK_ID | tail -n 1)
echo $PDB
cd $base_dir
cd $PDB
/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/phenix_prep.sh $PDB $NSLOTS $base_dir

