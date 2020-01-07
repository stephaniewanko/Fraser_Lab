#!/bin/bash


#________________________________________________INPUTS________________________________________________#
working_dir='/wynton/home/fraserlab/swankowicz/190430_Apo_Lig_Pairs'  #where the folders are located
apo_PDB_file=/wynton/home/fraserlab/swankowicz/190430_Apo_Lig_Pairs/List_isomorphous_pairs1.txt  #list of PDB IDs
holo_PDB_file=/wynton/home/fraserlab/swankowicz/190430_Apo_Lig_Pairs/List_isomorphous_pairs1.txt
output_dir='/wynton/home/fraserlab/swankowicz/190503_Targets/apo_holo_outputs/'

#________________________________________________Activate Env________________________________________________#
source /wynton/home/fraserlab/swankowicz/phenix-1.15.2-3472/phenix_env.sh
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate qfit
which python

#________________________________________________Qfit Analysis________________________________________________#
for i in {1..20}; do
  apo_PDB=$(cat $apo_PDB_file | head -n $i | tail -n 1)
  echo $apo_PDB
  cd $working_dir
  cd $apo_PDB
  echo 'qfit scripts'
  #generate_single_conformer $apo_PDB.pdb> baseline_summary_output.txt
  #get_metrics $apo_PDB.pdb > baseline_ind_rmsd_output.txt
  #generate_single_conformer multiconfomer2.pdb
  #python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/analysis.py -PDB=$apo_PDB
  
  holo_PDB=$(cat $holo_PDB_file | head -n $i | tail -n 1)
  echo $holo_PDB
  cd $working_dir
  cd $holo_PDB
  echo 'qfit scripts'
  #generate_single_conformer $holo_PDB.pdb> baseline_summary_output.txt
  #get_metrics $holo_PDB.pdb > baseline_ind_rmsd_output.txt
  lig_name=$(cat "ligand_name.txt")
  #python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/analysis.py -PDB=$holo_PDB #-sta=$lig_name -W ignore 
  cd $output_dir
  subset_structure -apo_structure ./$apo_PDB/$apo_PDB.pdb -holo_structure ./$holo_PDB/$holo_PDB.pdb -lig $lig_name -dis	5
  RMSF ../$apo_PDB/${apo_PDB}-sf.mtz $apo_PDB_subset.pdb --pdb=${apo_PDB}_5A
  RMSF ../$holo_PDB/${holo_PDB}-sf.mtz $holo_PDB_subset.pdb --pdb=${holo_PDB}_5A
  #${PDB}-sf.mtz $PDB.pdb --pdb=${PDB}_orig
done

