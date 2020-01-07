#!/bin/bash

#$ -l h_vmem=60G
#$ -l mem_free=60G
#$ -t 1-1
#$ -l h_rt=100:00:00
#$ -pe smp 8
#$ -R yes
#$ -V

#this script will run qfit based on the input PDB names you have.

#________________________________________________INPUTS________________________________________________#
working_dir='/wynton/home/fraserlab/swankowicz/high_res/' #'/wynton/home/fraserlab/swankowicz/high_res/' #'/wynton/group/fraser/swankowicz/Burnley_complete/' #'/wynton/home/fraserlab/swankowicz/high_res/'  #where the folders are located
PDB_file=/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/high_res_qfit.txt  #list of PDB IDs
echo $working_dir
export OMP_NUM_THREADS=1

#________________________________________________SET PATHS________________________________________________#
source /wynton/home/fraserlab/swankowicz/phenix-installer-dev-3594-intel-linux-2.6-x86_64-centos6/phenix-dev-3594/phenix_env.sh
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate qfit3


#________________________________________________CHECK VARIABLES________________________________________________#
echo $NSLOTS
which python
echo $SGE_TASK_ID


#________________________________________________RUN QFIT________________________________________________#
#PDB=$(cat $PDB_file | head -n $SGE_TASK_ID | tail -n 1)
PDB='2itn'
cd $working_dir
cd $PDB
echo $PDB

#phenix.composite_omit_map ${PDB}.mtz ${PDB}_0.6_5_tx1/1kzk_0.6_5_tx1_model_${SGE_TASK_ID}.pdb omit-type=refine nproc=$NSLOTS
#qfit_protein composite_omit_map.mtz -l 2FOFCWT,PH2FOFCWT ${PDB}_0.6_5_tx1/1kzk_0.6_5_tx1_model_${SGE_TASK_ID}.pdb -p $NSLOTS

phenix.composite_omit_map ${PDB}.mtz ${PDB}.pdb omit-type=refine nproc=$NSLOTS
qfit_protein composite_omit_map.mtz -l 2FOFCWT,PH2FOFCWT ${PDB}.pdb -p $NSLOTS
