#!/bin/bash

#$ -l h_vmem=80G
#$ -l mem_free=64G
#$ -t 1-13
#$ -l h_rt=100:00:00
#$ -pe smp 2
#$ -R yes
#$ -V

#________________________________________________INPUTS________________________________________________#
input_file=/wynton/group/fraser/swankowicz/191206_CA2_ens_refine/pdb_ids.txt
base_dir='/wynton/group/fraser/swankowicz/191206_CA2_ens_refine/amber/' #location of folders with PDB file
#base_dir='/wynton/group/fraser/swankowicz/amber_test/with_amber/'
export OMP_NUM_THREADS=1

#________________________________________________Activate Env________________________________________________#
echo 'nslots'
echo $NSLOTS
echo 'sge':
echo $SGE_TASK_ID
#source /wynton/home/fraserlab/swankowicz/phenix-1.15.2-3472/phenix_env.sh
#source /wynton/home/fraserlab/swankowicz/phenix-1.8.2-1309/phenix_env.sh
source /wynton/home/fraserlab/swankowicz/phenix-installer-dev-3594-intel-linux-2.6-x86_64-centos6/phenix-dev-3594/phenix_env.sh
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate phenix_ens
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

cp -R ${base_dir}/${PDB}/ $TMPDIR
cd $PDB



echo $PWD



#sh /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/phenix_prep.sh $PDB $NSLOTS $base_dir 
sh /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/phenix_prep_amber.sh $PDB $NSLOTS $base_dir
#qsub /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/grid_search_ens_refine.sh $PDB $base_dir

cp -R ${TMPDIR}/$PDB/ $base_dir/
#moving back to global disk
#:qmv * ~/$base_dir/$PDB/
