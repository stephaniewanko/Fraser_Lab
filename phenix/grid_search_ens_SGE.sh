#!/bin/bash

#$ -l h_vmem=80G
#$ -l mem_free=64G
#$ -l h_rt=100:00:00
#$ -pe smp 10
#$ -t 1-9

#grid search for ensemble_refinement
#Stephanie Wankowicz 4/15/2019


# we are going to do a grid search of a bunch of different
#perform grid search: pTLS: 1.0, 0.8, 0.6; weights: wxray_coupled_tbath_offset=2.5;5.0;10.0; timestep always 1.0
#put in job_title and output_dir based on grid search
#we are then going to determine which output is better and remove the files related to the poorer output.
cd /wynton/home/fraserlab/swankowicz/output/2pc0/

##TO ADD: Some log file with Rfree of all ensemble_refinements
PDB=$1
echo $PDB

options_file=/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/phenix_ens_grid_search_options.txt
_pTLS=$(cat $PDB_file | awk '{ print $1 }' head -n $SGE_TASK_ID | tail -n 1)
_weights=$(cat $PDB_file | awk '{ print $2 }'|head -n $SGE_TASK_ID | tail -n 1)

echo $_pTLS
echo $_weights

phenix.ensemble_refinement ${PDB}.updated_refine_001.pdb ${PDB}-sf.mtz elbow.${PDB}_pdb.001.cif pTLS=$_pTLS wxray_coupled_tbath_offset=$_weights ts=1.0 output_file_prefix=${PDB}.{$pTLS}.{$_we$

