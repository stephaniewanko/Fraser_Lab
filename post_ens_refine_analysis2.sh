#!/bin/bash
#Stephanie Wankowicz 6/3/2019
#post mortem ensemble refinement
source /wynton/home/fraserlab/swankowicz/phenix-installer-dev-3594-intel-linux-2.6-x86_64-centos6/phenix-dev-3594/phenix_env.sh
source activate qfit

base_dir=/wynton/group/fraser/swankowicz/new_phenix/
#base_dir=/wynton/group/fraser/swankowicz/
n=0
PDB_file=/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/paper_left_to_parse.txt
#PDB_file=/wynton/home/fraserlab/swankowicz/20190708_Ens_Paper/PDB_ids.txt
variable=''
while read line; do
  ((n++))
  echo $n

  PDB=$line
  cd $base_dir
  cd $PDB
  echo $PDB
  echo $PWD
  options_file=/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/phenix_ens_grid_search_options.txt
  for i in {1..45}; do
    pTLS=$(cat $options_file | awk '{ print $1 }' |head -n $i | tail -n 1)
    weights=$(cat $options_file | awk '{ print $2 }'|head -n $i | tail -n 1)
    tx=$(cat $options_file | awk '{ print $3 }'|head -n $i | tail -n 1)
    echo $tx
    if [ -e "${PDB}_${pTLS}_${weights}_${tx}" ]; then
      python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_refine_parser_main_log2.py ${PDB}_${pTLS}_${weights}_${tx}/${PDB}_${pTLS}_${weights}_${tx}.log ${PDB}_${pTLS}_${weights}_${tx}
      gunzip ${PDB}_${pTLS}_${weights}_${tx}/${PDB}_${pTLS}_${weights}_${tx}.pdb
      phenix.python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_rmsf.py ${PDB}_${pTLS}_${weights}_${tx}/${PDB}_${pTLS}_${weights}_${tx}.pdb CA csv > ${PDB}_${pTLS}_${weights}_${tx}_ens_RMSF.csv
    elif [ -d "${PDB}_${pTLS}_${weights}_${tx}" ]; then
      python /wyntion/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_refine_parser_main_log2.py ${PDB}_${pTLS}_${weights}_${tx}/${PDB}_${pTLS}_${weights}_${variable}_${tx}.log ${PDB}_${pTLS}_${weights}_${tx}
      gunzip ${PDB}_${pTLS}_${weights}_${tx}/${PDB}_${pTLS}_${weights}_${tx}.pdb
      phenix.python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_rmsf.py ${PDB}_${pTLS}_${weights}_${tx}/${PDB}_${pTLS}_${weights}_${tx}.pdb CA csv > ${PDB}_${pTLS}_${weights}_${tx}_ens_RMSF.csv
    else
      echo 'no file found'
    fi
  done
done <$PDB_file
