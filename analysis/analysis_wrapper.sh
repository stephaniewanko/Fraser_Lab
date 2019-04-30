#!/bin/bash


#________________________________________________INPUTS________________________________________________#
working_dir='/wynton/home/fraserlab/swankowicz/190430_Apo_Lig_Pairs'  #where the folders are located
PDB_file=/wynton/home/fraserlab/swankowicz/190430_Apo_Lig_Pairs/List_isomorphous_pairs1.txt  #list of PDB IDs


#________________________________________________Activate Env________________________________________________#
source /wynton/home/fraserlab/swankowicz/phenix-1.15.2-3472/phenix_env.sh
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate phenix_ens
which python

#________________________________________________RUN PHENIX________________________________________________#
for i in {1..2}; do
  PDB=$(cat $PDB_file | head -n $i | tail -n 1)

  echo $PDB
  cd $working_dir
  cd $PDB
  lig_name=$(cat "ligand_name.txt")
  python PDB_analysis.py -PDB=$PDB.pdb -sta=$lig_name
