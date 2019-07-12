
#!/bin/bash

#$ -l h_vmem=80G
#$ -l mem_free=64G
#$ -l h_rt=100:00:00
#$ -t 1-9

#grid search for ensemble_refinement
#Stephanie Wankowicz 
#4/30/2019

source /wynton/home/fraserlab/swankowicz/phenix-1.15.2-3472/phenix_env.sh
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate phenix_ens
which python
echo $SGE_TASK_ID


PDB=$1
cd /wynton/home/fraserlab/swankowicz/190430_Apo_Lig_Pairs/
echo $PDB
cd $PDB

options_file=/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/phenix_ens_grid_search_options.txt
_pTLS=$(cat $options_file | awk '{ print $1 }' |head -n $SGE_TASK_ID | tail -n 1)
_weights=$(cat $options_file | awk '{ print $2 }'|head -n $SGE_TASK_ID | tail -n 1)

echo '_pTLS'
echo $_pTLS
echo 'weights'
echo $_weights
echo $PWD
lig_name=$2
echo $lig_nam
output_file_name=${PDB}.$_pTLS.$_weights.
echo $output_file_name
mkdir $output_file_name
cd $output_file_name

if grep -F _refln.F_meas_au ../$PDB-sf.cif; then
   echo 'FOBS'
   phenix.ensemble_refinement ../${PDB}.updated_refine_001.pdb ../${PDB}-sf.mtz ../${PDB}.ligands.cif pTLS=$_pTLS wxray_coupled_tbath_offset=$_weights ts=1.0 output_file_prefix="$output_file_name" input.$
else
   echo 'SIGOBS'
   phenix.ensemble_refinement ../${PDB}.updated_refine_001.pdb ../${PDB}-sf.mtz ../${PDB}.ligands.cif pTLS=$_pTLS wxray_coupled_tbath_offset=$_weights ts=1.0 output_file_prefix="$output_file_name" input.$
fi



#phenix.ensemble_refinement ../${PDB}.updated_refine_001.pdb ../${PDB}-sf.mtz ../${PDB}.ligands.cif pTLS=$_pTLS wxray_coupled_tbath_offset=$_weights ts=1.0 output_file_prefix=$$
