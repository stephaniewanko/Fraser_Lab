#!/bin/bash

source /wynton/home/fraserlab/swankowicz/phenix-installer-dev-3594-intel-linux-2.6-x86_64-centos6/phenix-dev-3594/phenix_env.sh
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate qfit3
which python

#file=/wynton/group/fraser/swankowicz/test.txt 
#while read -r line; do
      line=$1
      pdb=$(echo ${line} | tr '[:upper:]' '[:lower:]')
      mid=$(echo ${pdb:1:2})
      echo $pdb
      echo $mid
      #cd /data/wankowicz/PDB_092019/${line}/
      cp /netapp/database/pdb/remediated/structure_factors/${mid}/r${pdb}sf.ent.gz /wynton/group/fraser/swankowicz/mtz/191114/
      #if grep -Fxq "Number of crystals" ${pdb}.dump; then
      #   echo 'already done'
      #else
      #echo 'redoing mtz dump'
      cd /wynton/group/fraser/swankowicz/mtz/191114/
      phenix.cif_as_mtz r${pdb}sf.ent.gz --ignore_bad_sigmas --extend_flags --merge
      phenix.mtz.dump r${pdb}sf.mtz > ${pdb}.dump
      #fi
done < $file
