#!/bin/bash
#Stephanie Wankowicz 6/3/2019
#post mortem ensemble refinement
source activate qfit

base_dir=/wynton/home/fraserlab/swankowicz/190503_Targets/
n=0
PDB_file=/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/apo_test.txt
while read line; do
  ((n++))
  echo $n
  PDB=$line
  cd $base_dir
  cd $PDB
  options=0
  options_file=/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/phenix_ens_grid_search_options.txt
  for i in {1..9}:
    pTLS=$(cat $options_file | awk '{ print $1 }' |head -n $i | tail -n 1)
    weights=$(cat $options_file | awk '{ print $2 }'|head -n $i | tail -n 1)
    if [ -e "${PDB}_${pTLS}_${weights}.pdb" ]; then
      python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_refine_parser_main_log.py ${PDB}_${pTLS}_${weights}/${PDB}_${pTLS}_${weights}.log
    else [ -d "${PDB}_${pTLS}_${weights}" ]; then
      python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_refine_parser_main_log.py ${PDB}_${pTLS}_${weights}/${PDB}_${pTLS}_${weights}.log
    fi
done <$PDB_file
