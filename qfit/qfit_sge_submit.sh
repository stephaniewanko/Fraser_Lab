#!/bin/bash

#$ -l h_vmem=20G
#$ -l mem_free=20G
#$ -t 01-12
#$ -l h_rt=100:00:00
#$ -pe smp 12
#$ -R yes
#$ -V

#this script will run qfit based on the input PDB names you have.

#________________________________________________INPUTS________________________________________________#
working_dir = /wynton/home/fraserlab/swankowicz/BRD4_output  #where the folders are located
PDB_file = /wynton/home/fraserlab/swankowicz/BRD4_output/test.txt  #list of PDB IDs



#________________________________________________SET PATHS________________________________________________#
source /wynton/home/fraserlab/swankowicz/phenix-1.15.2-3472/phenix_env.sh
export PATH = "/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate qfit


#________________________________________________CHECK VARIABLES________________________________________________#
echo $NSLOTS
which python
echo $SGE_TASK_ID



#________________________________________________CHECK VARIABLES________________________________________________#
PDB=$(cat $PDB_file | head -n $SGE_TASK_ID | tail -n 1)



#________________________________________________RUN QFIT________________________________________________#
cd $working_dir
cd $PDB
echo $PDB

phenix.composite_omit_map ${PDB}.mtz ${PDB}.pdb omit-type=refine nproc = $NSLOTS
qfit_protein composite_omit_map.mtz -l 2FOFCWT,PH2FOFCWT ${PDB}.pdb -p $NSLOTS

