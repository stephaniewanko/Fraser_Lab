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
  wget https://files.rcsb.org/download/${PDB}_phases.mtz
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
    phenix.ready_set pdb_file_name=$PDB.pdb cif_file_name=${PDB}_ligand > readyset_output.txt
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

  echo '________________________________________________________Validating the Ligand________________________________________________________'
  if [[ -e "elbow.${PDB}_pdb.001.cif" ]]; then  #only running this if we have a ligand
    mmtbx.validate_ligands ${PDB}.updated_refine_001.pdb ${PDB}-sf.mtz ligand_code="PGR" #"${PDB}_ligand" #prints out ADPs and occs + additional information
    phenix.pdb_interpretation ${PDB}.updated_refine_001.pdb write_geo=True
    elbow.refine_geo_display ${PDB}.updated_refine_001.pdb.geo PGR residual_histogram=True #prints out deviations including ligand specific RMSD and RMSz values
    #calculate the energy difference of the ligand in the model and it relaxed RM1/AM1, but can be linked to 3rd party packages
    phenix.reduce ${PDB}.updated_refine_001.pdb > ${PDB}.updated_refine_001_h.pdb
    phenix.elbow --chemical_component PGR --energy_validation=${PDB}.updated_refine_001_h.pdb
  fi



  echo '________________________________________________________Begin Ensemble Refinement_______________________________________________________'
  cont_var=$(cat "threshold.txt")
  echo $cont_var

  if [ "$cont_var" = "Passed1" ]; then
    phenix.ensemble_refinement ${PDB}.updated_refine_001.pdb ${PDB}-sf.mtz elbow.${PDB}_pdb.001.cif /Users/fraserlab/Documents/Stephanie/finalize.params
  else
    echo "Skipping Ensemble Refinement"
  fi
  #for structures with ligands, should use harmonic restraints harmonic_restraints.selections=’resname PO4 and element P’
done < $pdb_filelist
