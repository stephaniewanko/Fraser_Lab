#!/bin/bash

#$ -l h_vmem=20G
#$ -l mem_free=20G
#$ -t 1-5
#$ -l h_rt=100:00:00
#$ -pe smp 10
#$ -R yes
#$ -V

echo $NSLOTS

source /wynton/home/fraserlab/swankowicz/phenix-1.15.2-3472/phenix_env.sh
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate qfit
which python

echo $SGE_TASK_ID

PDB_file=/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/HIV_Prot2.txt

PDB=$(cat $PDB_file | head -n $SGE_TASK_ID | tail -n 1)

# Run qfit
cd /wynton/home/fraserlab/swankowicz/output
cd $PDB
echo $PDB
phenix.composite_omit_map ${PDB}.mtz ${PDB}.pdb omit-type=refine nproc = $NSLOTS
qfit_protein composite_omit_map.mtz -l 2FOFCWT,PH2FOFCWT ${PDB}.pdb -p $NSLOTS




