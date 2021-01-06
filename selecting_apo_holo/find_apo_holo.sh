#!/bin/bash

source /wynton/home/fraserlab/swankowicz/phenix-installer-dev-3594-intel-linux-2.6-x86_64-centos6/phenix-dev-3594/phenix_env.sh
export PATH="/wynton/home/fraserlab/swankowicz/anaconda3/bin:$PATH"
source activate qfit3
which python

#grep -v -x -f /data/wankowicz/PDB_092019/PDB_w_no_mtz.txt PDB_ID_2A_res.txt > PDB_ID_2A_res_wmtz.txt

if [[ -z "$TMPDIR" ]]; then
  if [[ -d /scratch ]]; then TMPDIR=/scratch/$USER; else TMPDIR=/tmp/$USER; fi
  mkdir -p "$TMPDIR"
  export TMPDIR
fi

#file=/home/wankowicz/scripts/PDB_IDs_w_lig.txt
   line=$1
   echo 'first' >> /wynton/group/fraser/swankowicz/pdbs_examined.txt
   echo $line >> /wynton/group/fraser/swankowicz/pdbs_examined.txt
   if grep -Fxq ${line} /wynton/group/fraser/swankowicz/nomtz_111419.txt; then
      #echo 'first no mtz'
      exit 1
   else
      line=$(echo ${line} | tr '[:upper:]' '[:lower:]')
      mid=$(echo ${line:1:2})
      echo $line
      #cd /data/wankowicz/PDB_092019/$line
      #phenix.mtz.dump ${line}.mtz
      #echo ${basedir_mtz}/${line}.dump
      if [ ! -f /wynton/group/fraser/swankowicz/mtz/mnt/data/u2/wankowicz/PDB_092019/fit/mtz_dumps/${line}.dump ]; then
         #echo $basedir_mtz
         echo $line > /wynton/group/fraser/swankowicz/nomtz_111419.txt
         #echo 'no mtz 2'
         continue
      else
         if [ ! -f pdb${line}.ent ]; then
             cp /netapp/database/pdb/remediated/pdb/${mid}/pdb${line}.ent.gz "$TMPDIR"
             gunzip pdb${line}.ent.gz
         fi
         SEQ1=$(/wynton/home/fraserlab/swankowicz/anaconda3/envs/qfit3/bin/python /wynton/group/fraser/swankowicz/get_seq.py pdb${line}.ent)
         RESO1=$(grep "^Resolution" ${line}.dump | head -n 1 | awk '{print $4}')
         RESO1_lower=$(echo ${RESO1}-0.1 | bc -l)
         RESO1_upper=$(echo ${RESO1}+0.1 | bc -l)
         echo $SEQ1
         if [ -z "$SEQ1" ]; then
            echo 'no sequence'
            exit 1
         fi
      fi
      file2=/wynton/group/fraser/swankowicz/PDB_ID_2A_res.txt
      for line2 in $(cat $file2); do
          line2=$(echo ${line2} | tr '[:upper:]' '[:lower:]')
          mid2=$(echo ${line2:1:2})
          #echo $line2 >> /wynton/group/fraser/swankowicz/pdbs_examined.txt
          if grep -Fxq ${line2} /wynton/group/fraser/swankowicz/PDB_2A_res_w_lig_111419.txt; then
             echo 'has ligand'
          elif grep -Fxq ${line2} /wynton/group/fraser/swankowicz/nomtz_111419.txt; then
             echo 'no mtz'
          elif  [ ! -f /wynton/group/fraser/swankowicz/mtz/mnt/data/u2/wankowicz/PDB_092019/fit/mtz_dumps/${line2}.dump ]; then
             echo $line2 > /wynton/group/fraser/swankowicz/nomtz_111419.txt
             echo 'no mtz 3'
          else
            if [ ! -f pdb${line2}.ent ]; then
             cp /netapp/database/pdb/remediated/pdb/${mid2}/pdb${line2}.ent.gz "$TMPDIR"
             gunzip pdb${line2}.ent.gz
            fi
            RESO2=$(grep "^Resolution" ${line2}.dump | head -n 1 | awk '{print $4}')
            SEQ2=$(/wynton/home/fraserlab/swankowicz/anaconda3/envs/qfit3/bin/python /wynton/group/fraser/swankowicz/get_seq.py pdb${line2}.ent)
            #echo $SEQ2
            if [[ -z "$SEQ2" ]]; then
               echo 'no sequence'
               continue
            else
              if [ "$SEQ1" = "$SEQ2" ]; then
                echo 'pair'
                echo $line
                echo $SEQ1
                echo $line2
                echo $SEQ2
                if (( `echo ${RESO2}'<='${RESO1_upper} | bc` )) && (( `echo ${RESO2}'>='${RESO1_lower} | bc` )); then
                   echo $line $line2 $RESO1 $RESO2 >> /wynton/group/fraser/swankowicz/PDB_pairs_191117.txt
                fi
              else
                SEQ1_end5=${SEQ1:-5}
                SEQ2_end5=${SEQ2:-5}
                SEQ1_begin5=${SEQ1:5}
                SEQ2_begin5=${SEQ2:5}
                if [ "$SEQ1" = "$SEQ2_begin5" ] || [ "$SEQ1" = "$SEQ2_end5" ] || [ "$SEQ2" = "$SEQ1_end5" ] || [ "$SEQ2" = "$SEQ1_begin5" ]; then
                   echo $line
                   echo $SEQ1
                   echo $line2
                   echo $SEQ2
                   if (( `echo ${RESO2}'<='${RESO1_upper} | bc` )) && (( `echo ${RESO2}'>='${RESO1_lower} | bc` )); then
                        echo $line $line2 $RESO1 $RESO2 >> /wynton/group/fraser/swankowicz/PDB_pairs_191117.txt
                   fi
                fi
              fi
            fi 
          fi
      done
   fi
done
