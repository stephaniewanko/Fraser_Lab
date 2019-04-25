#!/bin/bash

#$ -l h_vmem=80G
#$ -l mem_free=64G
#$ -t 1-5
#$ -l h_rt=100:00:00
#$ -pe smp 6
#$ -R yes
#$ -V

echo $NHOSTS

source /wynton/home/fraserlab/swankowicz/phenix-1.15.2-3472/phenix_env.sh
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate qfit
source activate phenix_ens
which python

input_file=/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/HIV_Prot2.txt
PDB=$(cat $PDB_file | head -n $SGE_TASK_ID | tail -n 1)
echo $PDB
cd /wynton/home/fraserlab/swankowicz/phenix_output/
mkdir $PDB
