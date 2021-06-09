#!/bin/bash
#set up a new refinement
'''
This script will take in a single PDB and MTZ file and run it through refinement procedure. This script is set up to be able to catch annomalies in many PDB files.
To run: ./phenix_prep.sh PDB_filename
'''

#source Phenix (This will allow you to run all the phenix commands.
export PHENIX_OVERWRITE_ALL=true #This allows phenix to overwrite the files outputted from a previous refinement run. 

PDB=$1 #$1 indicates that this is the first arguement after you run the script

echo $PDB #for output file, it is good to know what PDB you are connected to



#get ligand name and list of ligands for harmonic restraints
#~/anaconda3/envs/phenix_ens/bin/python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/PDB_ligand_parser.py $PDB /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ligands_to_remove.csv
#lig_name=$(cat "ligand_name.txt")
#echo $lig_name

echo '________________________________________________________Starting Phenix cif as mtz________________________________________________________'
phenix.cif_as_mtz $PDB-sf.cif --extend_flags --merge #convert PDB cif file to mtz file

echo '________________________________________________________Starting Phenix Ready Set________________________________________________________'
phenix.ready_set pdb_file_name=${PDB}.pdb  #this will establish cif files and get other things ready for refinement.


if [[ -e "${PDB}.ligands.cif" ]]; then 
    echo '________________________________________________________Running refinement with ligand.________________________________________________________'
    if grep -F _refln.F_meas_au $PDB-sf.cif; then #selecting FOBS or IOBS
        phenix.refine $PDB.updated.pdb $PDB-sf.mtz ${PDB}.ligands.cif refinement.input.xray_data.r_free_flags.label=R-free-flags /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/finalize.params refinement.input.xray_data.labels="FOBS,SIGFOBS"
    else
        echo 'IOBS'   
         phenix.refine $PDB.updated.pdb $PDB-sf.mtz ${PDB}.ligands.cif refinement.input.xray_data.r_free_flags.label=R-free-flags /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/finalize.params refinement.input.xray_data.labels="IOBS,SIGIOBS"
    fi
else
    echo '________________________________________________________Running refinement without ligand.________________________________________________________'
    if grep -F _refln.F_meas_au $PDB-sf.cif; then
        phenix.refine $PDB.updated.pdb $PDB-sf.mtz /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/finalize.params refinement.input.xray_data.labels="FOBS,SIGFOBS" refinement.input.xray_data.r_free_flags.label=R-free-flags
    else
        phenix.refine $PDB.updated.pdb $PDB-sf.mtz /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/finalize.params refinement.input.xray_data.r_free_flags.label=R-free-flags refinement.input.xray_data.labels="IOBS,SIGIOBS"
    fi
fi

echo '________________________________________________________Begin Ensemble Refinement_______________________________________________________'

