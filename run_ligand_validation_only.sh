#!/bin/bash
#set up a new refinement
#Stephanie Wankowicz 4/5/2019


#source Phenix
source /wynton/home/fraserlab/swankowicz/phenix-1.15.2-3472/phenix_env.sh #CHANGE THIS AS NEEDED

PDB_file=/wynton/home/fraserlab/swankowicz/190503_Targets/190503_Holo2.txt
while read line; do
  cd /wynton/home/fraserlab/swankowicz/190503_Targets
  echo $line
  PDB=$line
  #PDB=$1

  #make sure you are in the home directory
  #NSLOTS=$2
  echo $PDB
  cd $PDB
  rm 
  #get ligand name
  ~/anaconda3/envs/phenix_ens/bin/python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/PDB_ligand_parser.py $PDB /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ligands_to_remove.csv
  lig_name=$(cat "ligand_name.txt")
  echo $lig_name

  echo '________________________________________________________Validating the Ligand from Original PDB________________________________________________________'
  if [[ -e "${PDB}.ligands.cif" ]]; then  #only running this if we have a ligand
    echo $lig_name
    echo '________________________________________________________Phenix PDB Interpretation_______________________________________________________'
    phenix.pdb_interpretation ${PDB}.updated.pdb ${PDB}.ligands.cif write_geo=True
    echo '________________________________________________________Elbow Refine_Geo_Display_______________________________________________________'
    elbow.refine_geo_display ${PDB}.updated.pdb.geo $lig_name >> lig_RMSZ_pre_refine.txt #prints out deviations including ligand specific RMSD and RMSz values
  fi


  echo '________________________________________________________Validating the Ligand after Initial Refinement________________________________________________________'
  if [[ -e "${PDB}.ligands.cif" ]]; then  #only running this if we have a ligand
    echo '________________________________________________________Phenix PDB Interpretation_______________________________________________________'
    phenix.pdb_interpretation ${PDB}.updated_refine_001.pdb ${PDB}.ligands.cif write_geo=True
    echo '________________________________________________________Elbow Refine_Geo_Display_______________________________________________________'
    elbow.refine_geo_display ${PDB}.updated_refine_001.pdb.geo $lig_name >> lig_RMSZ_updated.txt
    #prints out deviations including ligand specific RMSD and RMSz values
    #calculate the energy difference of the ligand in the model and it relaxed RM1/AM1, but can be linked to 3rd party packages
  fi

  echo '________________________________________________________Validating Ligand Output_______________________________________________________'
  ~/anaconda3/envs/phenix_ens/bin/python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/lig_geo_parser.py -pre_refine=lig_RMSZ_pre_refine.txt -post_refine=lig_RMSZ_updated.txt -PDB=$PDB
done < $PDB_file
