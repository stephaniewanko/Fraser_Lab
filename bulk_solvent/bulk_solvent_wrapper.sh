#!/bin/bash
#Stephanie Wankowicz
#09/19/2019

source /home/wankowicz/phenix-installer-1.16-3546-intel-linux-2.6-x86_64-centos6/phenix-1.16-3546/phenix_env.sh
#________________________________________________INPUTS________________________________________________#
base_folder='/data/wankowicz/190815_qfit_done/'

pdb_filelist=/data/wankowicz/190815_qfit_done/refine_done_190919_PDB.txt
while read -r line; do
  PDB=$line
  cd $base_folder
  cd $PDB
  echo $PDB
  phenix.python /home/wankowicz/scripts/bulk_solvent/run_mosaic.py ${PDB}_single_conf.pdb ${PDB}_single_conf.mtz
  mv bulk_solvent.csv ${PDB}_single_conf_bulk_solvent.csv
done < $pdb_filelist
