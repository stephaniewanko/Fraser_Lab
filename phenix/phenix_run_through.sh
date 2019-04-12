#!/bin/bash
#set up a new refinement
#Stephanie Wankowicz 4/5/2019

##FOR i in 1..2, go though file and get the PDB, create new folder
#input: txt file with first column being pdb codes
home_dir=$PWD
echo $home_dir
pdb_filelist='190408_HIV_Prot2.txt'
#echo $pdb_filelist
#cat $pdb_filelist| while read line;
#while IFS=read line; do
#for i in $pdb_filelist;
while read line; do
  echo $line
  PDB=$line


  #make sure you are in the home directory
  cd $home_dir
  mkdir $PDB
  cd $PDB

  #download files
  wget https://files.rcsb.org/download/$PDB.pdb
  wget https://files.rcsb.org/download/$PDB-sf.cif

  #check to make sure your file exists. If it does not move onto the next item in the list.
  ##CHANGE THIS TO NOTIFY YOU!
  #if [ ! -f $PDB-sf.cif ]; then break; fi
  #if [ ! -f $PDB.pdb ]; then break; fi

  #pre-processing phenix
  echo '________________________________________________________Starting Phenix elbow________________________________________________________'
  phenix.elbow $PDB.pdb
  echo '________________________________________________________Starting Phenix cif as mtz________________________________________________________'
  phenix.cif_as_mtz $PDB-sf.cif --extend_flags

  echo '________________________________________________________Starting Phenix Ready Set________________________________________________________'
  if [[ -e "elbow.${PDB}_pdb.001.cif" ]]; then
    echo '________________________________________________________Running ready set with ligand.________________________________________________________'
    phenix.ready_set pdb_file_name=$PDB.pdb cif_file_name=elbow.${PDB}_pdb.001.cif
  else
    echo '________________________________________________________Running ready set without ligand.________________________________________________________'
    phenix.ready_set pdb_file_name=$PDB.pdb
  fi

  #run refinement
  if [[ -e "elbow.${PDB}_pdb.001.cif" ]]; then
    echo '________________________________________________________Running refinement with ligand.________________________________________________________'
    phenix.refine $PDB.updated.pdb $PDB-sf.mtz refinement.input.monomers="elbow.${PDB}_pdb.001.cif" /Users/fraserlab/Documents/Stephanie/finalize.params
  else
    echo '________________________________________________________Running refinement without ligand.________________________________________________________'
    phenix.refine $PDB.updated.pdb $PDB-sf.mtz /Users/fraserlab/Documents/Stephanie/finalize.params
  fi

  #get B-factors
  echo '________________________________________________________Starting Model versus Data________________________________________________________'
  phenix.model_vs_data ${PDB}.updated_refine_001.pdb $PDB-sf.cif
  #phenix.b_factor_statistics ${PDB}.updated_refine_001.pdb

  #extracting values from refinement log (we should have 001.log-> 010.log)
  echo '________________________________________________________Starting extract python script________________________________________________________'
  python /Users/fraserlab/Documents/Stephanie/Parse_refine_log.py ${PDB}.updated_refine_001.log

  echo '________________________________________________________Begin Ensemble Refinement_______________________________________________________'
  value=$(<threshold.txt)
  echo $value
  phenix.ensemble_refinement ${PDB}.updated.pdb ${PDB}-sf.mtz /Users/fraserlab/Documents/Stephanie/finalize.params refinement.input/monomers=elbow.${PDB}_pdb.001.cif
done < $pdb_filelist
