#!/bin/bash
#set up a new refinement
#Stephanie Wankowicz 4/5/2019

##FOR i in 1..2, go though file and get the PDB, create new folder
#input: txt file with first column being pdb codes

#source Phenix
source /Users/fraserlab/Documents/Stephanie/phenix-1.15.2-3472/build/bin/phenix #CHANGE THIS AS NEEDEd

home_dir=$PWD
echo $home_dir
pdb_filelist='190408_HIV_Prot2.txt'

#while read line; do
#  echo $line
#  PDB=$line
PDB=$1
NSLOTS=$2
echo $PDB

  #make sure you are in the home directory
cd $home_dir
mkdir $PDB
cd $PDB

  #download files
  #wget https://files.rcsb.org/download/$PDB.pdb
  #wget https://files.rcsb.org/download/$PDB-sf.cif
  #wget https://files.rcsb.org/download/${PDB}_phases.mtz
  #check to make sure your file exists. If it does not move onto the next item in the list.
  ##CHANGE THIS TO NOTIFY YOU!
  #if [ ! -f $PDB-sf.cif ]; then break; fi
  #if [ ! -f $PDB.pdb ]; then break; fi

  #get ligand name
~/anaconda3/envs/phenix_ens/bin/python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/PDB_ligand_parser.py $PDB /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ligands_to_re$
lig_name=$(cat "ligand_name.txt")
echo $lig_name

  #pre-processing phenix
echo '________________________________________________________Starting Phenix elbow________________________________________________________'
phenix.elbow $PDB.pdb --residue $lig_name --final_geometry
echo '________________________________________________________Starting Phenix cif as mtz________________________________________________________'
phenix.cif_as_mtz $PDB-sf.cif --extend_flags --merge

echo '________________________________________________________Starting Phenix Ready Set________________________________________________________'
phenix.ready_set pdb_file_name=$PDB.pdb #cif_file_name=elbow.${PDB}_pdb.001.cif > readyset_output.txt

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
        phenix.refine $PDB.updated.pdb $PDB-sf.mtz ${PDB}.ligands.cif refinement.input.xray_data.r_free_flags.label=R-free-flags /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/finalize$
    else
        echo 'SIGOBS'
         phenix.refine $PDB.updated.pdb $PDB-sf.mtz ${PDB}.ligands.cif refinement.input.xray_data.r_free_flags.label=R-free-flags /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/finaliz$
    fi
    #"elbow.${lig_name}.${PDB}_pdb.001.cif"
    # ${PDB}.ligands.cif
    ##refinement.input.monomers=elbow.${lig_name}.${PDB}_pdb.001.cif
  else
    echo '________________________________________________________Running refinement without ligand.________________________________________________________'
    if grep -F _refln.F_meas_au $PDB-sf.cif; then
        phenix.refine $PDB.updated.pdb $PDB-sf.mtz /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/finalize.params nproc=$NSLOTS refinement.input.xray_data.labels="FOBS,SIGFOBS" refinem$
    else
        phenix.refine $PDB.updated.pdb $PDB-sf.mtz /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/finalize.params nproc=$NSLOTS refinement.input.xray_data.r_free_flags.label=R-free-fla$
   fi
 fi

  #get B-factors
  echo '________________________________________________________Starting Model versus Data________________________________________________________'
  phenix.model_vs_data ${PDB}.updated_refine_001.pdb $PDB-sf.cif
  #phenix.b_factor_statistics ${PDB}.updated_refine_001.pdb

  #extracting values from refinement log (we should have 001.log-> 010.log)
  echo '________________________________________________________Starting extract python script________________________________________________________'
   ~/anaconda3/envs/phenix_ens/bin/python /Users/fraserlab/Documents/Stephanie/Parse_refine_log.py ${PDB}.updated_refine_001.log
  rm lig_RMSZ_updated.txt
  rm lig_RMSZ_pre_refine.txt
  
  echo '________________________________________________________Validating the Ligand from Original PDB________________________________________________________'
  if [[ -e "${PDB}.ligands.cif" ]]; then  #only running this if we have a ligand
    echo $lig_name

    #mmtbx.validate_ligands ${PDB}.pdb ${PDB}-sf.mtz ligand_code=$lig_name #"${PDB}_ligand" #prints out ADPs and occs + additional information
    echo '________________________________________________________Phenix PDB Interpretation_______________________________________________________'
    phenix.pdb_interpretation ${PDB}.pdb write_geo=True
    
    echo '________________________________________________________Elbow Refine_Geo_Display_______________________________________________________'
    elbow.refine_geo_display ${PDB}.pdb.geo $lig_name residual_histogram=True > ${PDB}_lig_RMSZ_pre_refine.txt #prints out deviations including ligand specific RMSD and RMSz values
    #calculate the energy difference of the ligand in the model and it relaxed RM1/AM1, but can be linked to 3rd party packages
    
    echo '________________________________________________________Phenix Reduce_______________________________________________________'
    phenix.reduce ${PDB}.pdb > ${PDB}_h.pdb
    
    echo '________________________________________________________Phenix Elbow_______________________________________________________'
    phenix.elbow --chemical_component $lig_name --energy_validation=${PDB}_h.pdb
  fi


  echo '________________________________________________________Validating the Ligand after Initial Refinement________________________________________________________'
  if [[ -e "elbow.${PDB}_pdb.001.cif" ]]; then  #only running this if we have a ligand
    echo '________________________________________________________Extracting the Ligand Name_______________________________________________________'

    mmtbx.validate_ligands ${PDB}.updated_refine_001.pdb ${PDB}-sf.mtz ligand_code=$lig_name #"${PDB}_ligand" #prints out ADPs and occs + additional information
    echo '________________________________________________________Phenix PDB Interpretation_______________________________________________________'
    phenix.pdb_interpretation ${PDB}.updated_refine_001.pdb write_geo=True
    echo '________________________________________________________Elbow Refine_Geo_Display_______________________________________________________'
    elbow.refine_geo_display ${PDB}.updated_refine_001.pdb.geo PGR residual_histogram=True > save.txt #prints out deviations including ligand specific RMSD and RMSz values
    #calculate the energy difference of the ligand in the model and it relaxed RM1/AM1, but can be linked to 3rd party packages
    echo '________________________________________________________Phenix Reduce_______________________________________________________'
    phenix.reduce ${PDB}.updated_refine_001.pdb> ${PDB}.h_updated_refine_001.pdb
    echo '________________________________________________________Phenix Elbow_______________________________________________________'
    phenix.elbow --chemical_component $lig_name --energy_validation=${PDB}.h_updated_refine_001.pdb
  fi

  echo '________________________________________________________Validating Ligand Output_______________________________________________________'
  ~/anaconda3/envs/phenix_ens/bin/python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/lig_geo_parser.py -pre_refine=lig_RMSZ_pre_refine.txt -post_refine=lig_RMSZ_updated.txt -PDB=$PDB



  echo '________________________________________________________Begin Ensemble Refinement_______________________________________________________'
  cont_var=$(cat "threshold.txt")
  echo $cont_var

  if [ "$cont_var" = "Passed" ]; then
    echo "testing"
    #sh /Users/fraserlab/Documents/Stephanie/grid_search_ens_refine.sh $PDB
    #phenix.ensemble_refinement ${PDB}.updated_refine_001.pdb ${PDB}-sf.mtz elbow.${PDB}_pdb.001.cif /Users/fraserlab/Documents/Stephanie/finalize.params
  else
    echo "Skipping Ensemble Refinement"
  fi
  #for structures with ligands, should use harmonic restraints harmonic_restraints.selections=’resname PO4 and element P’
done < $pdb_filelist
