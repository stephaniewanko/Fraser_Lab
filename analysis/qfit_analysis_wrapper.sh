#!/bin/bash


#________________________________________________INPUTS________________________________________________#
working_dir='/wynton/home/fraserlab/swankowicz/190430_Apo_Lig_Pairs'  #where the folders are located
apo_PDB_file=/wynton/home/fraserlab/swankowicz/190430_Apo_Lig_Pairs/List_isomorphous_pairs1.txt  #list of PDB IDs
holo_PDB_file=/wynton/home/fraserlab/swankowicz/190430_Apo_Lig_Pairs/List_isomorphous_pairs1.txt

#________________________________________________Activate Env________________________________________________#
source /wynton/home/fraserlab/swankowicz/phenix-1.15.2-3472/phenix_env.sh
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate phenix_ens
which python

#________________________________________________RUN PHENIX________________________________________________#


for i in {1..2}; do
  apo_PDB=$(cat $apo_PDB_file | head -n $i | tail -n 1)
  echo $apo_PDB
  cd $working_dir
  cd $apo_PDB
  echo 'qfit scripts'
  generate_single_conformer $apo_PDB.pdb> summary_output.txt
  get_metrics $apo_PDB.pdb > ind_rmsd_output.txt
  
  holo_PDB=$(cat $Holo_PDB_file | head -n $i | tail -n 1)
  echo $holo_PDB
  cd $working_dir
  cd $holo_PDB
  echo 'qfit scripts'
  generate_single_conformer $holo_PDB.pdb> summary_output.txt
  get_metrics $holo_PDB.pdb > ind_rmsd_output.txt
  lig_name=$(cat "ligand_name.txt")

  cd $working_dir
  cd $holo_PDB  
  lig_name=$(cat "ligand_name.txt")
  generate_single_conformer $holo_PDB.pdb> summary_output.txt
  get_metrics $holo_PDB.pdb > ind_rmsd_output.txt
  cd $working_dir
  subset_structure -apo_structure ./$apo_PDB/$apo_PDB.pdb -holo_structure ./$holo_PDB/$holo_PDB.pdb -lig $lig_name -dis	5
  python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/analysis.py -PDB=$holo_PDB #-sta=$lig_name -W ignore
done

