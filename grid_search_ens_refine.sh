#!/bin/bash

#$ -l h_vmem=80G
#$ -l mem_free=64G
#$ -l h_rt=100:00:00
#$ -t 1-45

#grid search for ensemble_refinement
#Stephanie Wankowicz 
#4/30/2019

#source /wynton/home/fraserlab/swankowicz/phenix-1.15.2-3472/phenix_env.sh
source /wynton/home/fraserlab/swankowicz/phenix-installer-dev-3594-intel-linux-2.6-x86_64-centos6/phenix-dev-3594/phenix_env.sh
#source /wynton/home/fraserlab/swankowicz/phenix-1.8.2-1309/phenix_env.sh
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate phenix_ens
which python



PDB=$1
base_dir=$2 #'/wynton/home/fraserlab/swankowicz/20190708_Ens_Paper/new_phenix/'
cd $working_dir
echo $PDB
cd $PDB

if [[ -z "$TMPDIR" ]]; then
  if [[ -d /scratch ]]; then TMPDIR=/scratch/$USER; else TMPDIR=/tmp/$USER; fi
  mkdir -p "$TMPDIR"
  export TMPDIR
fi

cd "$TMPDIR"

cp -R ${base_dir}/${PDB}/ $TMPDIR
cd $PDB

echo $PWD

options_file=/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/phenix_ens_grid_search_options.txt
_pTLS=$(cat $options_file | awk '{ print $1 }' |head -n $SGE_TASK_ID | tail -n 1)
_weights=$(cat $options_file | awk '{ print $2 }'|head -n $SGE_TASK_ID | tail -n 1)
_tx=$(cat $options_file | awk '{ print $3 }'|head -n $SGE_TASK_ID | tail -n 1)

echo '_pTLS'
echo $_pTLS
echo 'weights'
echo $_weights
echo 'tx'
echo $_tx
echo $PWD


lig_list=$(cat ${base_dir}/${PDB}/ligand_list.txt | rev | cut -c 5- | rev)



output_file_name="${PDB}"_"${_pTLS}"_"${_weights}"_${_tx}
echo $output_file_name

if [ -d "/$output_file_name" ]; then
   echo "Folder exists."
else
  mkdir $output_file_name
fi
cd $output_file_name

if [ -z "$lig_list" ]; then
   echo 'no ligand'
   if grep -F _refln.F_meas_au ../$PDB-sf.cif; then
     echo 'FOBS'
     phenix.ensemble_refinement ../${PDB}.updated_refine_001.pdb ../${PDB}-sf.mtz ../${PDB}.ligands.cif ptls=$_pTLS wxray_coupled_tbath_offset=$_weights output_file_prefix="$output_file_name" tx=$_tx input.xray_data.r_free_flags.generate=True input.xray_data.labels='F(+),SIGF(+),F(-),SIGF(-)' #use_amber=True
   else
     echo 'SIGOBS'
     phenix.ensemble_refinement ../${PDB}.updated_refine_001.pdb ../${PDB}-sf.mtz ../${PDB}.ligands.cif ptls=$_pTLS wxray_coupled_tbath_offset=$_weights output_file_prefix="$output_file_name" tx=$_tx input.xray_data.r_free_flags.generate=True input.xray_data.labels='F(+),SIGF(+),F(-),SIGF(-)' #use_amber=True
   fi
else
   echo 'ligand'
   if grep -F _refln.F_meas_au ../$PDB-sf.cif; then
     echo 'FOBS'
     phenix.ensemble_refinement ../${PDB}.updated_refine_001.pdb ../${PDB}-sf.mtz ../${PDB}.ligands.cif ptls=$_pTLS wxray_coupled_tbath_offset=$_weights harmonic_restraints.selections='"'"$lig_list"'"' output_file_prefix="$output_file_name" tx=$_tx input.xray_data.r_free_flags.generate=True input.xray_data.labels='F(+),SIGF(+),F(-),SIGF(-)' #use_amber=True
   else
     echo 'SIGOBS'
     phenix.ensemble_refinement ../${PDB}.updated_refine_001.pdb ../${PDB}-sf.mtz ../${PDB}.ligands.cif ptls=$_pTLS wxray_coupled_tbath_offset=$_weights harmonic_restraints.selections='"'"$lig_list"'"' output_file_prefix="$output_file_name" tx=$_tx input.xray_data.r_free_flags.generate=True input.xray_data.labels='F(+),SIGF(+),F(-),SIGF(-)' #use_amber=True #tx=$_tx use_amber=True
  fi
fi

cp -R ${TMPDIR}/$PDB/ $base_dir/
