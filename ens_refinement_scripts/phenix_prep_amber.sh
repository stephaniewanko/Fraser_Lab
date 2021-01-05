#!/bin/bash
#set up a new refinement
#Stephanie Wankowicz 4/5/2019
#git: 01-05-2021

#source Phenix
export PHENIX_OVERWRITE_ALL=true

PDB=$1

echo $PDB
echo $PWD  
  
#get ligand name and list of ligands for harmonic restraints
~/anaconda3/envs/phenix_ens/bin/python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/PDB_ligand_parser.py $PDB /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ligands_to_remove.csv
lig_name=$(cat "ligand_name.txt")
echo $lig_name

echo '________________________________________________________Starting Phenix cif as mtz________________________________________________________'
phenix.cif_as_mtz $PDB-sf.cif --extend_flags --merge

echo '________________________________________________________Starting Phenix Ready Set________________________________________________________'
phenix.ready_set pdb_file_name=${PDB}.pdb #cif_file_name=elbow.${lig_name}.${PDB}_pdb.001.cif >> readyset_output.txt

echo '________________________________________________________Prepping Amber________________________________________________________'
phenix.AmberPrep ${PDB}.updated.pdb 


  echo '________________________________________________________Checking on FOBS________________________________________________________'
  if grep -F _refln.F_meas_au $PDB-sf.cif; then
	echo 'FOBS'
  else
        echo 'IOBS'
  fi
  rm ${PDB}.updated_refine_*
  if [[ -e "${PDB}.ligands.cif" ]]; then
    echo '________________________________________________________Running refinement with ligand.________________________________________________________'
    if grep -F _refln.F_meas_au $PDB-sf.cif; then
        phenix.refine 4phenix_${PDB}.updated.pdb $PDB-sf.mtz ${PDB}.ligands.cif refinement.input.xray_data.r_free_flags.label=R-free-flags /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/finalize.params refinement.input.xray_data.labels="FOBS,SIGFOBS" use_amber=True amber.topology_file_name=4amber_${PDB}.updated.prmtop amber.coordinate_file_name=4amber_${PDB}.updated.rst7 amber.order_file_name=4amber_${PDB}.updated.order #print_amber_energies=True
    else
      	echo 'IOBS'   
	phenix.refine 4phenix_${PDB}.updated.pdb $PDB-sf.mtz ${PDB}.ligands.cif refinement.input.xray_data.r_free_flags.label=R-free-flags /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/finalize.params refinement.input.xray_data.labels="IOBS,SIGIOBS" use_amber=True amber.topology_file_name=4amber_${PDB}.updated.prmtop amber.coordinate_file_name=4amber_${PDB}.updated.rst7 amber.order_file_name=4amber_${PDB}.updated.order #print_amber_energies=True
    fi
  else
    echo '________________________________________________________Running refinement without ligand.________________________________________________________'
    if grep -F _refln.F_meas_au $PDB-sf.cif; then
	phenix.refine 4phenix_${PDB}.updated.pdb $PDB-sf.mtz refinement.input.xray_data.r_free_flags.label=R-free-flags /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/finalize.params refinement.input.xray_data.labels="FOBS,SIGFOBS" use_amber=True amber.topology_file_name=4amber_${PDB}.updated.prmtop amber.coordinate_file_name=4amber_${PDB}.updated.rst7 amber.order_file_name=4amber_${PDB}.updated.order #print_amber_energies=True
    else
	phenix.refine 4phenix_${PDB}.updated.pdb $PDB-sf.mtz refinement.input.xray_data.r_free_flags.label=R-free-flags /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/finalize.params refinement.input.xray_data.labels="IOBS,SIGIOBS" use_amber=True amber.topology_file_name=4amber_${PDB}.updated.prmtop amber.coordinate_file_name=4amber_${PDB}.updated.rst7 amber.order_file_name=4amber_${PDB}.updated.order #print_amber_energies=True
   fi
 fi
 
qsub /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/grid_search_ens_refine.sh $PDB $3

