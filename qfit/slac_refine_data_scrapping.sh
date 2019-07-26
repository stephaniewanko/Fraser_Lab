#!/bin/bash
#Stephanie Wankowicz
#07/25/2019

#this must be done before you submit to SGE since SGE cannot connect to the internet!
source /home/wankowicz/phenix-installer-1.16-3546-intel-linux-2.6-x86_64-centos6/phenix-1.16-3546/phenix_env.sh

conda activate qfit

#________________________________________________INPUTS________________________________________________#
base_folder='/mnt/data/u2/wankowicz/190719_PDBs/' #base folder (where you want to put folders/pdb files)

pdb_filelist=/mnt/home1/wankowicz/190709_qfit/test.txt  #list of pdb files
while read -r line; do
  PDB=$line
  cd $PDB
  python /mnt/home1/wankowicz/scripts/parse_refine_log.py -log_file ${PDB}_original_rerefined.log -PDB ${PDB} -type org_qfit_refine
  python /mnt/home1/wankowicz/scripts/parse_refine_log.py -log_file ${PDB}_original_rerefined.log -PDB ${PDB} -type post_qfit_refine
  #get original data
  #outputs
done < $pdb_filelist

