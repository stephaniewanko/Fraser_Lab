#!/bin/bash

#$ -l h_vmem=80G
#$ -l mem_free=64G
#$ -t 1-2000
#$ -l h_rt=100:00:00
#$ -pe smp 2
#$ -R yes
#$ -V

source /wynton/home/fraserlab/swankowicz/phenix-installer-dev-3594-intel-linux-2.6-x86_64-centos6/phenix-dev-3594/phenix_env.sh
export PHENIX_OVERWRITE_ALL=true

input_file=/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/targets_191028.txt
base_dir='/wynton/group/fraser/swankowicz/190503_Targets/'

PDB=$(cat $input_file | head -n $SGE_TASK_ID | tail -n 1)

cd $base_dir
cd $PDB
~/anaconda3/envs/phenix_ens/bin/python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/Parse_refine_log.py -log_file ${PDB}.updated_refine_001.log -PDB $PDB
