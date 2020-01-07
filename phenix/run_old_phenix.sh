#!/bin/bash
#set up a new refinement
#Stephanie Wankowicz 4/5/2019
#git 07-12-2019

#source Phenix
#source /wynton/home/fraserlab/swankowicz/phenix-1.15.2-3472/phenix_env.sh #CHANGE THIS AS NEEDED
source /wynton/home/fraserlab/swankowicz/phenix-1.8.2-1309/phenix_env.sh

PDB=$1

NSLOTS=$2
echo $PDB

#get ligand name
~/anaconda3/envs/phenix_ens/bin/python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/PDB_ligand_parser.py $PDB /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ligands_to_remove.csv
lig_name=$(cat "ligand_name.txt")
echo $lig_name

echo '________________________________________________________Starting Phenix cif as mtz________________________________________________________'
phenix.cif_as_mtz $PDB-sf.cif --extend_flags --merge

echo '________________________________________________________Starting Phenix Ready Set________________________________________________________'
phenix.ready_set pdb_file_name=$PDB.pdb #cif_file_name=elbow.${lig_name}.${PDB}_pdb.001.cif >> readyset_output.txt

echo '________________________________________________________Checking on FOBS________________________________________________________'
  if grep -F _refln.F_meas_au $PDB-sf.cif; then
        echo 'FOBS'
  else
      	echo 'SIGOBS'
  fi
  rm ${PDB}.updated_refine_*
  if [[ -e "${PDB}.ligands.cif" ]]; then
    echo '________________________________________________________Running refinement with ligand.________________________________________________________'
    if grep -F _refln.F_meas_au $PDB-sf.cif; then
        phenix.refine $PDB.updated.pdb $PDB-sf.mtz ${PDB}.ligands.cif refinement.input.xray_data.r_free_flags.label=R-free-flags /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/finalize.params nproc=$NSLOTS refinement.input.xray_data.labels="FOBS,SIGFOBS"
    else
        echo 'SIGOBS'
         phenix.refine $PDB.updated.pdb $PDB-sf.mtz ${PDB}.ligands.cif refinement.input.xray_data.r_free_flags.label=R-free-flags /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/finalize.params nproc=$NSLOTS refinement.input.xray_data.labels="IOBS,SIGIOBS"
    fi
 fi









phenix.ensemble_refinement ../${PDB}.updated_refine_001.pdb ../${PDB}-sf.mtz ../${PDB}.ligands.cif wxray_coupled_tbath_offset=$_weights output_file_prefix="$output_file_name"
