#!/bin/bash

#$ -l h_vmem=4G
#$ -l mem_free=4G
#$ -t 1-1
#$ -l h_rt=10:00:00
#$ -pe smp 1
#$ -R yes
#$ -V

#________________________________________________INPUTS________________________________________________#
input_file=/wynton/group/fraser/swankowicz/191206_CA2_ens_refine/pdb_ids.txt #list of PDB files
base_dir='/wynton/group/fraser/swankowicz/191206_CA2_ens_refine/amber/' #location of folders with PDB file
export OMP_NUM_THREADS=1

#________________________________________________Activate Env________________________________________________#
source #PHENIX
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate phenix_ens #conda enviornment 
which python

#________________________________________________RUN PHENIX________________________________________________#
PDB=$(cat $input_file | head -n $SGE_TASK_ID | tail -n 1)
echo $PDB
cd $base_dir
cd $PDB

#____________________________________________MOVING TO SCRATCH_____________________________________________#
if [[ -z "$TMPDIR" ]]; then
  if [[ -d /scratch ]]; then TMPDIR=/scratch/$USER; else TMPDIR=/tmp/$USER; fi
  mkdir -p "$TMPDIR"
  export TMPDIR
fi

cd "$TMPDIR"

cp -R ${base_dir}/${PDB}/ ${TMPDIR}
cd $PDB

#sh /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/phenix_prep.sh $PDB $NSLOTS $base_dir 
sh /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/phenix_prep_amber.sh $PDB $NSLOTS $base_dir
#qsub /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/grid_search_ens_refine.sh $PDB $base_dir

cp -R ${TMPDIR}/$PDB/ $base_dir/ #moving back to global disk
