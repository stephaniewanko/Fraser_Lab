[wankowicz@smbnxs1 ~/scripts]$ vi run_mtz_dump.sh

#!/bin/bash

source /home/wankowicz/phenix-installer-1.16-3546-intel-linux-2.6-x86_64-centos6/phenix-1.16-3546/phenix_env.sh
export PATH="/home/wankowicz/anaconda3/bin:$PATH"
source activate qfit2.1
which python

file=/data/wankowicz/PDB_092019/fit/list_mtz.txt
while read -r line; do
   #if grep -Fxq ${line} /data/wankowicz/PDB_092019/PDB_w_no_mtz.txt; then
   #   continue
   #else
      pdb=$(echo ${line:10:4})
      mid=$(echo ${line:11:2})
      echo $pdb
      echo $mid
      #cd /data/wankowicz/PDB_092019/${line}/
      cd /data/wankowicz/PDB_092019/fit/mtz/${mid}/
      if grep -Fxq "Number of crystals" ${pdb}.dump; then
         echo 'already done'
      else
         echo 'redoing mtz dump'
         phenix.cif_as_mtz r${pdb}sf.ent.gz --ignore_bad_sigmas --extend_flags --merge
         phenix.mtz.dump r${pdb}sf.mtz > ${pdb}.dump
      fi
   #fi
done < $file
