#!/bin/bash
#$ -l h_vmem=20G
#$ -l mem_free=20G
#$ -t 1-398
#$ -l h_rt=100:00:00
#$ -pe smp 1
#$ -R yes
#$ -V

#________________________________________________INPUTS________________________________________________#
working_dir='/wynton/home/fraserlab/swankowicz/190503_Targets/'  #where the folders are located
#PDB_file=/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/paired_5232019_3.txt   #list of PDB IDs
PDB_file=/wynton/home/fraserlab/swankowicz/190503_Targets/190503_Holo.txt

#________________________________________________Activate Env________________________________________________#
echo $SGE_TASK_ID
source /wynton/home/fraserlab/swankowicz/phenix-1.15.2-3472/phenix_env.sh
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate phenix_ens
which python

#________________________________________________RUN PHENIX________________________________________________#
PDB=$(cat $PDB_file | head -n $SGE_TASK_ID | tail -n 1)

echo $PDB
cd $working_dir
cd $PDB
/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/determine_finished.sh $PDB

