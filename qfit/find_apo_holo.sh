#!/bin/bash

source /home/wankowicz/phenix-installer-1.16-3546-intel-linux-2.6-x86_64-centos6/phenix-1.16-3546/phenix_env.sh
#export PATH="/home/wankowicz/anaconda3/bin:$PATH"
source activate qfit2.1
which python

#grep -v -x -f /data/wankowicz/PDB_092019/PDB_w_no_mtz.txt PDB_ID_2A_res.txt > PDB_ID_2A_res_wmtz.txt

basedir_mtz='/data/sauloho/databases/PDB/mtzs'

file=/home/wankowicz/scripts/PDB_IDs_w_lig_101419_sdc01.txt
for line in $(cat $file); do
   echo 'first' >> pdbs_examined_sdc01.txt
   echo $line >> pdbs_examined_sdc01.txt
   if grep -Fxq ${line} /data/wankowicz/PDB_092019/nomtz_101419.txt; then
      #echo 'first no mtz'
      continue
   else
      line=$(echo ${line} | tr '[:upper:]' '[:lower:]')
      mid=$(echo ${line:1:2})
      echo $line
      #cd /data/wankowicz/PDB_092019/$line
      #phenix.mtz.dump ${line}.mtz
      #echo ${basedir_mtz}/${line}.dump
      if [ ! -f /data/wankowicz/PDB_092019/fit/mtz/${mid}/${line}.dump ]; then
         #echo $basedir_mtz
         echo $line > /data/wankowicz/PDB_092019/nomtz_101419.txt
         #echo 'no mtz 2'
         continue
      else
         SPACE1=$(grep "^Space group number from file:" /data/wankowicz/PDB_092019/fit/mtz/${mid}/${line}.dump | awk '{print $6}')
         UNIT1=$(grep "Unit cell:" /data/wankowicz/PDB_092019/fit/mtz/${mid}/${line}.dump | tail -n 1 | sed "s/[(),]//g" | awk '{print $3,$4,$5,$6,$7,$8}')
         RESO1=$(grep "^Resolution" /data/wankowicz/PDB_092019/fit/mtz/${mid}/${line}.dump | head -n 1 | awk '{print $4}')
         SEQ1=$(grep ${line}_A -A 1 /data/wankowicz/PDB_092019/pdb_seqres.txt | tail -n 1)
      fi
      file2=/mnt/home1/wankowicz/scripts/PDB_ID_2A_res.txt
      for line2 in $(cat $file2); do
          line2=$(echo ${line2} | tr '[:upper:]' '[:lower:]')
          mid2=$(echo ${line2:1:2})
          echo $line2
          echo $line2 >> pdbs_examined_sdc03.txt
          if grep -Fxq ${line2} /home/wankowicz/scripts/PDB_IDs_w_lig_101419.txt; then
             continue
          elif grep -Fxq ${line2} /data/wankowicz/PDB_092019/nomtz_101419.txt; then
             continue
             #echo 'no mtz'
          elif  [ ! -f /data/wankowicz/PDB_092019/fit/mtz/${mid2}/${line2}.dump ]; then
             echo $line2 > /data/wankowicz/PDB_092019/nomtz_101419.txt
             #echo 'no mtz 3'
             continue
          elif [ ! -f /data/sauloho/databases/PDB/${mid2}/${line2}.fasta.txt ]; then
             continue
          else
             #cd /data/wankowicz/PDB_092019/$line2
             SPACE2=$(grep "^Space group number from file:i" /data/wankowicz/PDB_092019/fit/mtz/${mid2}/${line2}.dump | awk '{print $6}')
             UNIT2=$(grep "Unit cell:" /data/wankowicz/PDB_092019/fit/mtz/${mid2}/${line2}.dump | tail -n 1 | sed "s/[(),]//g" | awk '{print $3,$4,$5,$6,$7,$8}')
             RESO2=$(grep "^Resolution" /data/wankowicz/PDB_092019/fit/mtz/${mid2}/${line2}.dump | head -n 1 | awk '{print $4}')
             SEQ2=$(grep ${line2}_A -A 1 /data/wankowicz/PDB_092019/pdb_seqres.txt | tail -n 1)
             if [ "$SEQ1" = "$SEQ2" ]; then
                echo 'pair'
                #echo $SEQ2
                echo $line $line2 $RESO1 $RESO2 >> /data/wankowicz/PDB_092019/PDB_pairs_191015_sdc01.txt
             else
                SEQ1_end5=${SEQ1:-5}
                SEQ2_end5=${SEQ2:-5}
                SEQ1_begin5=${SEQ1:5}
                SEQ2_begin5=${SEQ2:5}
                if [ "$SEQ1" = "$SEQ2_begin5" ] || [ "$SEQ1" = "$SEQ2_end5" ] || [ "$SEQ2" = "$SEQ1_end5" ] || [ "$SEQ2" = "$SEQ1_begin5" ]; then
                     echo 'pair'
                     echo $line $line2 $RESO1 $RESO2 >> /data/wankowicz/PDB_092019/PDB_pairs_191015_sdc01.txt
                fi
             fi
          fi
      done
   fi
done

