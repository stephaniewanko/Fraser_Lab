#!/bin/bash
#Stephanie Wankowicz 6/3/2019
#post mortem ensemble refinement
source /wynton/home/fraserlab/swankowicz/phenix-installer-dev-3594-intel-linux-2.6-x86_64-centos6/phenix-dev-3594/phenix_env.sh
source activate qfit

#base_dir=/wynton/home/fraserlab/swankowicz/20190708_Ens_Paper/new_phenix/
base_dir=/wynton/group/fraser/swankowicz/new_phenix/
n=0
PDB_file=/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/new_phenix_pdb.txt
variable='Burnley_paper'
while read line; do
  ((n++))
  echo $n

  PDB=$line
  cd $base_dir
  cd $PDB
  echo $PDB
  echo $PWD
  options_file=/wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/phenix_ens_grid_search_options.txt
  for i in {1..9}; do
    pTLS=$(cat $options_file | awk '{ print $1 }' |head -n $i | tail -n 1)
    weights=$(cat $options_file | awk '{ print $2 }'|head -n $i | tail -n 1)
    if [ -e "${PDB}_${pTLS}_${weights}_${variable}" ]; then
      python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_refine_parser_main_log2.py ${PDB}_${pTLS}_${weights}_${variable}/${PDB}_${pTLS}_${weights}_${variable}.log $variable
      gunzip ${PDB}_${pTLS}_${weights}_${variable}/${PDB}_${pTLS}_${weights}_${variable}.pdb.gz
      phenix.python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_rmsf.py ${PDB}_${pTLS}_${weights}_${variable}/${PDB}_${pTLS}_${weights}_${variable}.pdb CA csv > ${PDB}_${pTLS}_${weights}_${variable}_ens_RMSF.csv
    elif [ -d "${PDB}_${pTLS}_${weights}_${variable}" ]; then
      python /wyntion/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_refine_parser_main_log2.py ${PDB}_${pTLS}_${weights}_${variable}/${PDB}_${pTLS}_${weights}_${variable}.log $variable
      gunzip ${PDB}_${pTLS}_${weights}_${variable}/${PDB}_${pTLS}_${weights}_${variable}.pdb.gz
      phenix.python /wynton/home/fraserlab/swankowicz/190419_Phenix_ensemble/ens_rmsf.py ${PDB}_${pTLS}_${weights}_${variable}/${PDB}_${pTLS}_${weights}_${variable}.pdb CA csv > ${PDB}_${pTLS}_${weights}_${variable}_ens_RMSF.csv
    else
      echo 'no file found'
    fi
  done
done <$PDB_file
