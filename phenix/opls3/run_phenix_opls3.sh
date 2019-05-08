#!/bin/bash
#set up a new refinement w/ OPLS3E
#Stephanie Wankowicz 05/07/2019

#source Phenix & SCHRODINGER
source /wynton/home/fraserlab/swankowicz/phenix-1.15.2-3472/phenix_env.sh #CHANGE THIS AS NEEDED
source $SCHRODINGER

pdb_names='names.txt'
while read line; do
  echo $line
  PDB=$line

  #make sure you are in the home directory
  echo $PDB
  echo '________________________________________________________Downloading Files________________________________________________________'
  #download files
  wget https://files.rcsb.org/download/$PDB.pdb
  wget https://files.rcsb.org/download/$PDB-sf.cif
  wget http://edmaps.rcsb.org/coefficients/$PDB.mtz

  echo '________________________________________________________Grabbing Ligand Name________________________________________________________'
  #get ligand name
  python PDB_parser.py $PDB ligands_to_remove.csv
  lig_name=$(cat "ligand_name.txt")
  echo $lig_name

  echo '_______________________________________________________Running SCHRODINGER Prep________________________________________________________'
  $SCHRODINGER/run ../gydo_run_phenix_ensemble_refinement_SW.py --struct_file=${PDB}.pdb --mtz_file=${PDB}.mtz --ligand=$lig_name

  echo '_______________________________________________________Running Readyset________________________________________________________'
  phenix.ready_set ${PDB}.pdb actions.optimise_final_geometry_of_hydrogens=False

  echo '_______________________________________________________Combine Readyset & OPLS3 Ligand________________________________________________________'
  $SCHRODINGER/run ../gydo_run_phenix_ensemble_refinement_SW.py --struct_file=${PDB}.pdb --mtz_file=${PDB}.mtz --ligand=$lig_name

  echo '_______________________________________________________Run Ensemble Refinement________________________________________________________'
  #add in grid Search
  phenix.ensemble_refinement ../${PDB}.updated_refine_001.pdb ../${PDB}-sf.mtz ../${PDB}.ligands.cif pTLS=$_pTLS wxray_coupled_tbath_offset=$_weights ts=1.0 output_file_prefix="$output_file_name"
