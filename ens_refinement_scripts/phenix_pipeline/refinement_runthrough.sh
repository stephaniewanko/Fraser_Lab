!/bin/bash
#set up a new refinement
#updated: 2020-01-20

#source Phenix
export PHENIX_OVERWRITE_ALL=true

PDB=$1

NSLOTS=$2 #number of cores avaliable
echo $PDB
echo $PWD  

#get large ligand name and list of ligands for harmonic restraints
python PDB_ligand_parser.py $PDB ligands_to_remove.csv

lig_name=$(cat "ligand_name.txt")
echo $lig_name

echo '________________________________________________________Starting Phenix cif as mtz________________________________________________________'
phenix.cif_as_mtz $PDB-sf.cif --extend_flags --merge

echo '________________________________________________________Starting Phenix Ready Set________________________________________________________'
phenix.ready_set pdb_file_name=$PDB.pdb 

echo '________________________________________________________Checking on FOBS________________________________________________________'
if grep -F _refln.F_meas_au $PDB-sf.cif; then
        echo 'FOBS'
else
        echo 'IOBS'
fi

if [[ -e "${PDB}.ligands.cif" ]]; then
echo '________________________________________________________Running refinement with ligand.________________________________________________________'
    if grep -F _refln.F_meas_au $PDB-sf.cif; then
        phenix.refine $PDB.updated.pdb $PDB-sf.mtz ${PDB}.ligands.cif finalize.params nproc=$NSLOTS #refinement.input.xray_data.r_free_flags.label=R-free-flags refinement.input.xray_data.labels="FOBS,SIGFOBS"
    else
        echo 'IOBS'   
        phenix.refine $PDB.updated.pdb $PDB-sf.mtz ${PDB}.ligands.cif finalize.params nproc=$NSLOTS #refinement.input.xray_data.r_free_flags.label=R-free-flags refinement.input.xray_data.labels="IOBS,SIGIOBS"
    fi
    
else
    echo '________________________________________________________Running refinement without ligand.________________________________________________________'
    if grep -F _refln.F_meas_au $PDB-sf.cif; then
        phenix.refine $PDB.updated.pdb $PDB-sf.mtz finalize.params nproc=$NSLOTS #refinement.input.xray_data.labels="FOBS,SIGFOBS" refinement.input.xray_data.r_free_flags.label=R-free-flags 
    else
        phenix.refine $PDB.updated.pdb $PDB-sf.mtz finalize.params nproc=$NSLOTS #refinement.input.xray_data.r_free_flags.label=R-free-flags refinement.input.xray_data.labels="IOBS,SIGIOBS"
   fi
 fi

echo '________________________________________________________Starting Model versus Data________________________________________________________'
phenix.model_vs_data ${PDB}.updated_refine_001.pdb $PDB-sf.cif > ${PDB}_model_v_data.txt

echo '________________________________________________________Starting extract python script________________________________________________________'
python Parse_refine_log.py -log_file ${PDB}.updated_refine_001.log -PDB $PDB

echo '________________________________________________________Validating the Ligand from Original PDB________________________________________________________'
  if [[ -e "${PDB}.ligands.cif" ]]; then  #only running this if we have a ligand    
    
    echo $lig_name
    #mmtbx.validate_ligands ${PDB}.pdb ${PDB}-sf.mtz ligand_code=$lig_name #"${PDB}_ligand" #prints out ADPs and occs + additional information
    
    echo '________________________________________________________Phenix PDB Interpretation_______________________________________________________'
    phenix.pdb_interpretation ${PDB}.updated.pdb ${PDB}.ligands.cif write_geo=True
    
    echo '________________________________________________________Elbow Refine_Geo_Display_______________________________________________________'
    elbow.refine_geo_display ${PDB}.updated.pdb.geo $lig_name >> lig_RMSZ_pre_refine.txt #prints out deviations including ligand specific RMSD and RMSz values
  fi


echo '________________________________________________________Validating the Ligand after Initial Refinement________________________________________________________'
  if [[ -e "${PDB}.ligands.cif" ]]; then  #only running this if we have a ligand
    #mmtbx.validate_ligands ${PDB}.updated_refine_001.pdb ${PDB}-sf.mtz ligand_code=$lig_name #"${PDB}_ligand" #prints out ADPs and occs + additional information
    
    echo '________________________________________________________Phenix PDB Interpretation_______________________________________________________'
    phenix.pdb_interpretation ${PDB}.updated_refine_001.pdb ${PDB}.ligands.cif write_geo=True
    
    echo '________________________________________________________Elbow Refine_Geo_Display_______________________________________________________'
    elbow.refine_geo_display ${PDB}.updated_refine_001.pdb.geo $lig_name >> lig_RMSZ_updated.txt
    #prints out deviations including ligand specific RMSD and RMSz values
    #calculate the energy difference of the ligand in the model and it relaxed RM1/AM1, but can be linked to 3rd party packages
  fi

  echo '________________________________________________________Validating Ligand Output_______________________________________________________'
  python lig_geo_parser.py -pre_refine=lig_RMSZ_pre_refine.txt -post_refine=lig_RMSZ_updated.txt -PDB=$PDB


  echo '________________________________________________________Begin Ensemble Refinement_______________________________________________________'
  qsub grid_search_ens_refine.sh $PDB $3

