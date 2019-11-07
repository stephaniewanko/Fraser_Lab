#!/bin/bash
#Stephanie Wankowicz
#07/25/2019

#this must be done before you submit to SGE since SGE cannot connect to the internet!
#source /home/wankowicz/phenix-installer-1.16-3546-intel-linux-2.6-x86_64-centos6/phenix-1.16-3546/phenix_env.sh
#________________________________________________INPUTS________________________________________________#
base_folder='/data/wankowicz/190815_qfit_done/'

pdb_filelist=/data/wankowicz/190815_qfit_done/refine_done_PDB_190922.txt  #list of pdb files
while read -r line; do
  PDB=$line
  cd $base_folder
  cd $PDB
  echo $PDB
  #head ${PDB}_qfit.pdb
  #if [ -f ${PDB}_004.pdb ]; then 
  #   echo 'almost done'
  #elif [ -f ${PDB}_003.pdb ]; then
  #   echo 'working on zeros'
  #else
  #   echo 'get this thing going!'
  #fi 
  python /home/wankowicz/scripts/parse_refine_log.py -log_file=${PDB}_single_conf.log -PDB=$PDB -type=single_conf_pair
  python /home/wankowicz/scripts/parse_refine_log.py -log_file=${PDB}_qFit.log -PDB=$PDB -type=qfit_pair
done < $pdb_filelist
